import logging
import datetime
from collections import OrderedDict
from smtplib import SMTPException

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
