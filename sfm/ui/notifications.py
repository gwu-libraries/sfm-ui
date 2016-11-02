import logging
import datetime
from collections import OrderedDict
from smtplib import SMTPException
from subprocess import check_output, CalledProcessError

from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from .models import User, CollectionSet, Collection, HarvestStat
from .sched import next_run_time

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
            line_units = filter(None, line.split(' '))
            # the sfm-data and sfm-processing mount at sfm-data,
            # we only need to count the sfm-data
            if line_units:
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
        except CalledProcessError, e:
            log.error("%s returned %s: %s", cmd, e.returncode, e.output)
        return res

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
    # get sfm-data info
    data_monitor = MonitorSpace(settings.SFM_DATA_DIR, settings.DATA_THRESHOLD)
    data_list.append(data_monitor.get_space_info())
    # get sfm-processing info
    processing_monitor = MonitorSpace(settings.SFM_PROCESSING_DIR, settings.PROCESSING_THRESHOLD)
    data_list.append(processing_monitor.get_space_info())
    return data_list


def send_free_space_emails(superusers=None):
    log.info("Sending free space emails")
    msg_cache = {}

    if superusers is None:
        superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        if _should_send_space_email(user, msg_cache):
            msg = _create_space_email(user, msg_cache)
            try:
                log.debug("Sending email to %s: %s", msg.to, msg.subject)
                msg.send()
            except SMTPException, ex:
                log.error("Error sending email: %s", ex)
        else:
            log.debug("Not sending email to %s", user.username)


def _should_send_space_email(user, msg_cache):
    if not user.is_superuser or not user.email:
        return False
    # get the space mem
    msg_cache['space_data'] = get_free_space()
    # if any volume need send email, return true
    return any(msg['send_email'] for msg in msg_cache['space_data'])


def _create_space_email(user, msg_cache):
    text_template = get_template('email/free_space_email.txt')
    html_template = get_template('email/free_space_email.html')
    msg_cache["url"] = _create_url(reverse('home'))
    d = Context(msg_cache)
    msg = EmailMultiAlternatives("[WARNING] Low free space on SFM server",
                                 text_template.render(d), settings.EMAIL_HOST_USER, [user.email])
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
            except SMTPException, ex:
                log.error("Error sending email: %s", ex)
        else:
            log.debug("Not sending email to %s", user.username)


def _should_send_email(user, date=None):
    if date is None:
        date = datetime.date.today()
    send_email = False
    has_active_collections = Collection.objects.filter(collection_set__group__in=user.groups.all(),
                                                       is_active=True).exists()
    if user.email and has_active_collections:
        if user.email_frequency == User.DAILY:
            send_email = True
        elif user.email_frequency == User.MONTHLY and date.day == 1:
            send_email = True
        elif user.email_frequency == User.WEEKLY and date.weekday() == 6:
            send_email = True
    return send_email


def _create_email(user, collection_set_cache):
    text_template = get_template('email/user_harvest_email.txt')
    html_template = get_template('email/user_harvest_email.html')
    d = Context(_create_context(user, collection_set_cache))
    msg = EmailMultiAlternatives("Update on your Social Feed Manager harvests", text_template.render(d),
                                 settings.EMAIL_HOST_USER, [user.email])
    msg.attach_alternative(html_template.render(d), "text/html")
    return msg


def _create_context(user, collection_set_cache):
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    prev_day = today + datetime.timedelta(days=-2)
    # Greater than this date
    last_7_start = yesterday + datetime.timedelta(days=-7)
    prev_7_start = yesterday + datetime.timedelta(days=-14)
    last_30_start = yesterday + datetime.timedelta(days=-30)
    prev_30_start = yesterday + datetime.timedelta(days=-60)
    # Less than or equal to this date
    last_7_end = yesterday
    prev_7_end = last_7_start
    last_30_end = yesterday
    prev_30_end = last_30_start
    c = {
        "url": _create_url(reverse('home'))
    }
    # Ordered list of collection sets
    collection_sets = OrderedDict()
    for collection_set in CollectionSet.objects.filter(group__in=user.groups.all()).order_by('name'):
        # Using a cache to avoid regenerating the data repeatedly.
        if collection_set in collection_set_cache:
            collections = collection_set_cache[collection_set]
        else:
            collections = OrderedDict()
            for collection in Collection.objects.filter(collection_set=collection_set).order_by('name'):
                collection_info = {
                    "url": _create_url(reverse('collection_detail', args=(collection.id,)))
                }
                if collection.is_active:
                    collection_info['next_run_time'] = next_run_time(collection.id)
                    stats = {}
                    # Yesterday
                    _add_stats(stats, 'yesterday', HarvestStat.objects.filter(harvest__collection=collection,
                                                                              harvest_date=yesterday).values(
                        'item').annotate(count=Sum('count')))
                    # Prev day
                    _add_stats(stats, 'prev_day', HarvestStat.objects.filter(harvest__collection=collection,
                                                                             harvest_date=prev_day).values(
                        'item').annotate(count=Sum('count')))
                    # Last 7
                    _add_stats(stats, 'last_7', HarvestStat.objects.filter(harvest__collection=collection,
                                                                           harvest_date__gt=last_7_start,
                                                                           harvest_date__lte=last_7_end).values(
                        'item').annotate(count=Sum('count')))
                    # Prev 7
                    _add_stats(stats, 'prev_7', HarvestStat.objects.filter(harvest__collection=collection,
                                                                           harvest_date__gt=prev_7_start,
                                                                           harvest_date__lte=prev_7_end).values(
                        'item').annotate(count=Sum('count')))
                    # Last 30
                    _add_stats(stats, 'last_30', HarvestStat.objects.filter(harvest__collection=collection,
                                                                            harvest_date__gt=last_30_start,
                                                                            harvest_date__lte=last_30_end).values(
                        'item').annotate(count=Sum('count')))
                    # Prev 7
                    _add_stats(stats, 'prev_30', HarvestStat.objects.filter(harvest__collection=collection,
                                                                            harvest_date__gt=prev_30_start,
                                                                            harvest_date__lte=prev_30_end).values(
                        'item').annotate(count=Sum('count')))
                    collection_info['stats'] = stats
                collections[collection] = collection_info

            collection_set_cache[collection_set] = collections
        collection_sets[collection_set] = {
            "collections": collections,
            "url": _create_url(reverse('collection_set_detail', args=(collection_set.id,)))

        }
    c['collection_sets'] = collection_sets
    return c


def _add_stats(stats, name, result_set):
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


def _create_url(path):
    return 'http://{}{}'.format(Site.objects.get_current().domain, path)
