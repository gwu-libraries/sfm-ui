import datetime
from rabbitmq_admin import AdminAPI
from django.conf import settings
from .models import Harvest, Export
import logging

log = logging.getLogger(__name__)

def monitor_harvests():
    # From 3 days ago to the present. This will omit old activity.
    # Excludes when status is REQUESTED.
    # Note that this can't be tested since SQLite doesn't support.
    return Harvest.objects \
        .exclude(status=Harvest.REQUESTED) \
        .filter(date_updated__gt=(datetime.datetime.utcnow() - datetime.timedelta(days=3))) \
        .order_by('service', 'host', 'instance', '-id').distinct('service', 'host', 'instance')


def monitor_exports():
    # From 3 days ago to the present. This will omit old activity.
    # Excludes when status is REQUESTED.
    # Note that this can't be tested since SQLite doesn't support.
    return Export.objects \
        .exclude(status=Export.REQUESTED) \
        .filter(date_updated__gt=(datetime.datetime.utcnow() - datetime.timedelta(days=3))) \
        .order_by('service', 'host', 'instance', '-id') \
        .distinct('service', 'host', 'instance')


def monitor_queues():
    api = QueueAPI(url='http://{}:{}'.format(settings.RABBITMQ_HOST, settings.RABBITMQ_MANAGEMENT_PORT),
                   auth=(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD))
    return api.list_queues()


class QueueAPI(AdminAPI):
    def list_queues(self):
        harvester_queues = {}
        exporter_queues = {}
        ui_queues = {}
        for queue in self._api_get("/api/queues"):
            queue_name = queue["name"].replace("_", " ").title()
            if queue_name.endswith("Harvester") or queue_name.endswith("Priority"):
                harvester_queues[queue_name] = queue.get("messages", 0)
            elif queue_name.endswith("Exporter"):
                exporter_queues[queue_name] = queue.get("messages", 0)
            elif queue_name.endswith("Ui"):
                ui_queues[queue_name] = queue.get("messages", 0)
        return harvester_queues, exporter_queues, ui_queues
