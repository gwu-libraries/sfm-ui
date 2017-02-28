from django.apps import AppConfig
from rabbit import RabbitWorker
from django.db.models.signals import post_save, pre_delete, m2m_changed, post_delete
from django.conf import settings
import logging

log = logging.getLogger(__name__)


class UIConfig(AppConfig):
    name = 'ui'
    verbose_name = "ui"

    def ready(self):
        RabbitWorker().declare_exchange()
        from models import Collection, Export, CollectionSet, Warc
        from sched import start_sched, schedule_harvest_receiver, unschedule_harvest_receiver
        from export import export_receiver, export_m2m_receiver
        from notifications import send_user_harvest_emails, send_free_space_emails, send_queue_warn_emails
        from serialize import serialize_all
        from models import delete_collection_set_receiver, delete_collection_receiver, delete_warc_receiver, \
            delete_export_receiver

        if settings.SCHEDULE_HARVESTS:
            log.debug("Setting receivers for collections.")
            post_save.connect(schedule_harvest_receiver, sender=Collection)
            pre_delete.connect(unschedule_harvest_receiver, sender=Collection)

        # Export
        if settings.PERFORM_EXPORTS:
            log.debug("Setting receiver for exports.")
            post_save.connect(export_receiver, sender=Export)
            m2m_changed.connect(export_m2m_receiver, sender=Export.seeds.through)

        # Add 5 minute interval
        if settings.FIVE_MINUTE_SCHEDULE:
            log.debug("Adding 5 minute timer")
            Collection.SCHEDULE_CHOICES.append((5, "Every 5 minutes"))

        # Add 5 minute interval
        if settings.HUNDRED_ITEM_SEGMENT:
            log.debug("Adding 10 item export segment")
            Export.SEGMENT_CHOICES.append((100, "100"))

        # Add weibo search collection
        if settings.WEIBO_SEARCH_OPTION:
            log.debug("Adding weibo search collection")
            Collection.HARVEST_CHOICES.append(('weibo_search', 'Weibo search'))
            Collection.HARVEST_DESCRIPTION.append(('weibo_search', 'Recent Weibo posts matching a query'))

        if settings.RUN_SCHEDULER:
            log.debug("Running scheduler")
            sched = start_sched()

            # User harvest emails
            if settings.PERFORM_USER_HARVEST_EMAILS:
                if sched.get_job('user_harvest_emails') is not None:
                    sched.remove_job('user_harvest_emails')
                sched.add_job(send_user_harvest_emails, 'cron', hour=settings.USER_HARVEST_EMAILS_HOUR,
                              minute=settings.USER_HARVEST_EMAILS_MINUTE, id='user_harvest_emails')

            # scheduled job to monitor the free space
            if settings.PERFORM_SCAN_FREE_SPACE:
                if sched.get_job('scan_free_space') is not None:
                    sched.remove_job('scan_free_space')
                sched.add_job(send_free_space_emails, 'interval', hours=int(settings.SCAN_FREE_SPACE_HOUR_INTERVAL),
                              id='scan_free_space')

            # scheduled job to check monitor queue message
            if settings.PERFORM_MONITOR_QUEUE:
                if sched.get_job('monitor_queue_length') is not None:
                    sched.remove_job('monitor_queue_length')
                sched.add_job(send_queue_warn_emails, 'interval', hours=int(settings.MONITOR_QUEUE_HOUR_INTERVAL),
                              id='monitor_queue_length')

            # Serialization
            if settings.PERFORM_SERIALIZE:
                if sched.get_job('serialize') is not None:
                    sched.remove_job('serialize')
                sched.add_job(serialize_all, 'cron', hour=settings.SERIALIZE_HOUR,
                              minute=settings.SERIALIZE_MINUTE, id='serialize')

        else:
            log.debug("Not running scheduler")

        # Delete files
        log.debug("Setting delete receivers")
        post_delete.connect(delete_collection_set_receiver, sender=CollectionSet)
        post_delete.connect(delete_collection_receiver, sender=Collection)
        post_delete.connect(delete_warc_receiver, sender=Warc)
        post_delete.connect(delete_export_receiver, sender=Export)