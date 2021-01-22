import logging
from datetime import date, datetime, timedelta, time
from collections import OrderedDict
from smtplib import SMTPException
from subprocess import check_output, CalledProcessError
import pytz
from itertools import chain

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum, Q
from django.conf import settings
from django.urls import reverse

from .models import User, CollectionSet, Collection, HarvestStat, Harvest
from .sched import next_run_time
from .utils import get_admin_email_addresses, get_site_url
from . import monitoring

log = logging.getLogger(__name__)


class MonitorSpace(object):
    def __init__(self, volume_dir, threshold):
        """
        A class for monitor free space of the special directory
        :param volume_dir: the volume mounted directory, considered as the id of the record.
        :param threshold: the free space threshold.
        :return:
        """
        # deal with the empty string
        if not volume_dir:
            volume_dir = 'None'
        if not threshold:
            threshold = '10GB'

        self.space_msg_cache = {'volume_id': volume_dir, 'threshold': threshold, 'bar_color': 'progress-bar-success'}

    def analysis_space(self):
        """
        Getting space info from 'df -h'
        """
        total_free_space = total_space = 0
        res = self.run_check_cmd()
        split_lines = res.split('\n')
        for line in split_lines:
            line_units = list(filter(None, line.split(' ')))
            # the sfm-data and sfm-processing mount at sfm-data,
            # we only need to count the sfm-data
            if line_units:
                # The following uncommented code will not work anymore, '/sfm-data' was removed and replaced by '/sfm-db-data', '/sfm-mq-data' etc
                # get rid of the unit at the space,12M
                # eg:['/dev/sda1', '208074M', '47203M', '150279M', '24%', '/sfm-data']
                total_free_space = int(line_units[3][:-1])
                total_space = int(line_units[1][:-1])
        self.space_msg_cache['total_space'] = self._size_readable_fmt(total_space)
        self.space_msg_cache['total_free_space'] = self._size_readable_fmt(total_free_space)
        self.space_msg_cache['percentage'] = 0 if not total_space else int(
            float(total_space - total_free_space) / float(total_space) * 100)
        # update bar color with percentage
        self.space_msg_cache['bar_color'] = self._get_bar_color(self.space_msg_cache['percentage'])
        return total_free_space

    def get_space_info(self):
        """
        get the space info and check whether to send email
        """
        self.space_msg_cache['send_email'] = False

        # get the free space info
        total_free_space = self.analysis_space()

        # if not available info return False
        if self.space_msg_cache['total_space'] == '0.0MB':
            return self.space_msg_cache

        # deal with the configuration
        suffix = self.space_msg_cache['threshold'][-2:]
        if suffix not in {'MB', 'GB', 'TB'}:
            log.error("Free Space threshold %s, configure suffix error.",
                      self.space_msg_cache['threshold'])
            return self.space_msg_cache

        # get rid of the unit and deal with GB/TB, compare with MB
        space_threshold = int(self.space_msg_cache['threshold'][:-2])
        if suffix == 'GB':
            space_threshold *= 1024
        elif suffix == 'TB':
            space_threshold *= 11048576

        log.debug("total space %s, space threshold %s,", self.space_msg_cache['total_free_space'],
                  self.space_msg_cache['threshold'])

        if total_free_space < space_threshold:
            self.space_msg_cache['send_email'] = True
        return self.space_msg_cache

    def run_check_cmd(self):
        cmd = "df -h -BM {volume_id} | grep -w {volume_id}".format(volume_id=self.space_msg_cache['volume_id'])
        res = ''
        try:
            res = check_output(cmd, shell=True)
            log.debug("Running %s completed.", cmd)
        except CalledProcessError as e:
            log.error("%s returned %s: %s", cmd, e.returncode, e.output)
        return res.decode('utf-8')

    @staticmethod
    def _size_readable_fmt(num, suffix='B'):
        for unit in ['M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Y', suffix)

    @staticmethod
    def _get_bar_color(percentage):
        if 70 <= percentage <= 80:
            return 'progress-bar-warning'
        elif percentage > 80:
            return 'progress-bar-danger'
        return 'progress-bar-success'


def get_free_space():
    """
    an interface to get the space info
    :return: a space data list
    """
    data_list = []
    # get data directories info (sfm-db-data, sfm-mq-data, sfm-export-data, sfm-containers-data and sfm-collection-set-data)
    data_db_monitor = MonitorSpace(settings.SFM_DB_DATA_DIR, settings.DATA_THRESHOLD_DB)
    data_mq_monitor = MonitorSpace(settings.SFM_MQ_DATA_DIR, settings.DATA_THRESHOLD_MQ)
    data_export_monitor = MonitorSpace(settings.SFM_EXPORT_DATA_DIR, settings.DATA_THRESHOLD_EXPORT)
    data_containers_monitor = MonitorSpace(settings.SFM_CONTAINERS_DATA_DIR, settings.DATA_THRESHOLD_CONTAINERS)
    data_collection_set_monitor = MonitorSpace(settings.SFM_COLLECTION_SET_DATA_DIR, settings.DATA_THRESHOLD_COLLECTION_SET)

    data_list.append(data_db_monitor.get_space_info())
    data_list.append(data_mq_monitor.get_space_info())
    data_list.append(data_export_monitor.get_space_info())
    data_list.append(data_containers_monitor.get_space_info())
    data_list.append(data_collection_set_monitor.get_space_info())

    # get sfm-processing info
    processing_monitor = MonitorSpace(settings.SFM_PROCESSING_DIR, settings.PROCESSING_THRESHOLD)
    data_list.append(processing_monitor.get_space_info())
    return data_list


def send_free_space_emails():
    log.info("Sending free space emails")
    msg_cache = {
        # get the space mem
        'space_data': get_free_space()
    }

    if _should_send_space_email(msg_cache):
        email_addresses = get_admin_email_addresses()
        for email_address in email_addresses:
            msg = _create_space_email(email_address, msg_cache)
            try:
                log.debug("Sending email to %s: %s", msg.to, msg.subject)
                msg.send()
            except SMTPException as ex:
                log.error("Error sending email: %s", ex)
            except IOError as ex:
                log.error("Error sending email: %s", ex)


def _should_send_space_email(msg_cache):
    # if any volume need send email, return true
    return any(msg['send_email'] for msg in msg_cache['space_data'])


def _create_space_email(email_address, msg_cache):
    text_template = get_template('email/free_space_email.txt')
    html_template = get_template('email/free_space_email.html')
    msg_cache["url"] = _create_url(reverse('home'))
    d = msg_cache
    msg = EmailMultiAlternatives("[WARNING] Low free space on SFM server",
                                 text_template.render(d), settings.EMAIL_FROM, [email_address])
    msg.attach_alternative(html_template.render(d), "text/html")
    return msg


def get_queue_data():
    queue_threshold_map = settings.QUEUE_LENGTH_THRESHOLD
    queue_threshold_other = settings.QUEUE_LENGTH_THRESHOLD_OTHER
    return get_warn_queue(queue_threshold_map, queue_threshold_other)


def get_warn_queue(q_th_map, q_th_other):
    hqs, eqs, uqs = monitoring.monitor_queues()

    # filter any msg count larger than the threshold
    return list(filter(lambda x: x[1] >= int(q_th_map[x[0]] if x[0] in q_th_map else q_th_other),
                       chain(hqs.items(), eqs.items(), uqs.items())))


def send_queue_warn_emails():
    log.info("Sending queue length warning emails")
    # get queue data and determine whether to send email
    msg_cache = {
        'queue_data': get_queue_data()
    }

    if len(msg_cache['queue_data']):
        email_addresses = get_admin_email_addresses()
        for email_address in email_addresses:
            msg = _create_queue_warn_email(email_address, msg_cache)
            try:
                log.debug("Sending email to %s: %s", msg.to, msg.subject)
                msg.send()
            except SMTPException as ex:
                log.error("Error sending email: %s", ex)
            except IOError as ex:
                log.error("Error sending email: %s", ex)


def _create_queue_warn_email(email_address, msg_cache):
    text_template = get_template('email/queue_length_email.txt')
    html_template = get_template('email/queue_length_email.html')
    msg_cache["url"] = _create_url(reverse('home'))
    msg_cache["monitor_url"] = _create_url(reverse('monitor'))
    d = msg_cache
    msg = EmailMultiAlternatives("[WARNING] Long message queue on SFM server",
                                 text_template.render(d), settings.EMAIL_FROM, [email_address])
    msg.attach_alternative(html_template.render(d), "text/html")
    return msg


def send_user_harvest_emails(users=None):
    log.info("Sending user harvest emails")
    collection_set_cache = {}
    if users is None:
        users = User.objects.all()
    for user in users:
        if _should_send_email(user):
            msg = _create_email(user, collection_set_cache)
            try:
                log.debug("Sending email to %s: %s", msg.to, msg.subject)
                msg.send()
            except SMTPException as ex:
                log.error("Error sending email: %s", ex)
            except IOError as ex:
                log.error("Error sending email: %s", ex)

        else:
            log.debug("Not sending email to %s", user.username)


def _should_send_email(user, today=None):
    if today is None:
        today = date.today()
    send_email = False
    has_active_collections = Collection.objects.filter(collection_set__group__in=user.groups.all(),
                                                       is_on=True).exists()
    if user.email and has_active_collections:
        if user.email_frequency == User.DAILY:
            send_email = True
        elif user.email_frequency == User.MONTHLY and today.day == 1:
            send_email = True
        elif user.email_frequency == User.WEEKLY and today.weekday() == 6:
            send_email = True
    return send_email


def _create_email(user, collection_set_cache):
    text_template = get_template('email/user_harvest_email.txt')
    html_template = get_template('email/user_harvest_email.html')
    d = _create_context(user, collection_set_cache)
    msg = EmailMultiAlternatives("Update on your Social Feed Manager harvests", text_template.render(d),
                                 settings.EMAIL_FROM, [user.email])
    msg.attach_alternative(html_template.render(d), "text/html")
    return msg


def _create_context(user, collection_set_cache):
    # Start and end are datetimes. The range is inclusive.
    today = datetime.utcnow().date()

    # Yesterday
    yesterday = today + timedelta(days=-1)
    yesterday_start = datetime.combine(yesterday,
                                       time(time.min.hour, time.min.minute, time.min.second, tzinfo=pytz.utc))
    yesterday_end = datetime.combine(yesterday, time(time.max.hour, time.max.minute, time.max.second, tzinfo=pytz.utc))

    # Previous day
    prev_day_start = yesterday_start + timedelta(days=-1)
    prev_day_end = yesterday_end + timedelta(days=-1)

    last_7_start = yesterday_start + timedelta(days=-6)
    last_7_end = yesterday_end

    prev_7_start = last_7_start + timedelta(days=-7)
    prev_7_end = yesterday_end + timedelta(days=-7)

    last_30_start = yesterday_start + timedelta(days=-29)
    last_30_end = yesterday_end

    prev_30_start = last_30_start + timedelta(days=-30)
    prev_30_end = last_30_end + timedelta(days=-30)

    time_ranges = (
        ('yesterday', yesterday_start, yesterday_end),
        ('prev_day', prev_day_start, prev_day_end),
        ('last_7', last_7_start, last_7_end),
        ('prev_7', prev_7_start, prev_7_end),
        ('last_30', last_30_start, last_30_end),
        ('prev_30', prev_30_start, prev_30_end)
    )

    c = {
        "url": _create_url(reverse('home'))
    }
    # Ordered list of collection sets
    collection_sets = OrderedDict()
    for collection_set in CollectionSet.objects.filter(group__in=user.groups.all()).filter(
            collections__is_active=True).order_by('name'):
        # Using a cache to avoid regenerating the data repeatedly.
        if collection_set in collection_set_cache:
            collections = collection_set_cache[collection_set]
        else:
            collections = OrderedDict()
            for collection in Collection.objects.filter(collection_set=collection_set).filter(is_active=True).order_by(
                    'name'):
                collection_info = {
                    "url": _create_url(reverse('collection_detail', args=(collection.id,)))
                }
                if collection.is_on:
                    collection_info['next_run_time'] = next_run_time(collection.id)
                    stats = {}
                    for name, range_start, range_end in time_ranges:
                        _add_stats(stats, name, collection, range_start, range_end)
                    for name, range_start, range_end in time_ranges:
                        _update_stats_for_na(stats, name, collection, range_start, range_end)

                    collection_info['stats'] = stats
                collections[collection] = collection_info

            collection_set_cache[collection_set] = collections
        collection_sets[collection_set] = {
            "collections": collections,
            "url": _create_url(reverse('collection_set_detail', args=(collection_set.id,)))

        }
    c['collection_sets'] = collection_sets
    return c


def _add_stats(stats, name, collection, range_start, range_end):
    result_set = HarvestStat.objects.filter(harvest__collection=collection,
                                            harvest_date__gte=range_start.date(),
                                            harvest_date__lte=range_end.date()).values(
        'item').annotate(count=Sum('count'))
    for result in result_set:
        item = result['item']
        if item not in stats:
            stats[item] = {
                'yesterday': 0,
                'prev_day': 0,
                'last_7': 0,
                'prev_7': 0,
                'last_30': 0,
                'prev_30': 0
            }
        stats[item][name] = result['count']


def _update_stats_for_na(stats, name, collection, range_start, range_end):
    for item, item_stats in stats.items():
        if item != "web resource" and item_stats[name] == 0 and not _was_harvest_in_range(range_start, range_end,
                                                                                          collection):
            item_stats[name] = "N/A"


def _was_harvest_in_range(range_start, range_end, collection):
    # Harvests that have start and end (i.e., completed)
    if Harvest.objects.filter(Q(collection=collection)
                              & Q(date_started__isnull=False)
                              & Q(date_ended__isnull=False)
                              & (Q(date_started__range=(range_start, range_end))
                                 | Q(date_ended__range=(range_start, range_end))
                                 | (Q(date_started__lt=range_start) & Q(date_ended__gt=range_end)))
                              & ~Q(harvest_type='web')).exists():
        return True
    # Harvests that are still running
    # Using status=RUNNING to try to filter out some
    if Harvest.objects.filter(Q(collection=collection)
                              & Q(status=Harvest.RUNNING)
                              & Q(date_started__isnull=False)
                              & Q(date_ended__isnull=True)
                              & Q(date_started__range=(range_start, range_end))
                              & ~Q(harvest_type='web')).exists():
        return True
    return False


def _create_url(path):
    return get_site_url() + path
