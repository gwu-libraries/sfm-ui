from django.apps import AppConfig
from rabbit import RabbitWorker
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.conf import settings
import logging

log = logging.getLogger(__name__)


class UIConfig(AppConfig):
    name = 'ui'
    verbose_name = "ui"

    def ready(self):
        RabbitWorker().declare_exchange()
        from models import Collection, Export
        from sched import start_sched, schedule_harvest_receiver, unschedule_harvest_receiver
        from export import export_receiver, export_m2m_receiver

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

        if settings.RUN_SCHEDULER:
            log.debug("Running scheduler")
            start_sched()
        else:
            log.debug("Not running scheduler")
