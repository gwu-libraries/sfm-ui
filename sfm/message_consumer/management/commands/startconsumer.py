from django.conf import settings
from django.core.management.base import BaseCommand
from message_consumer.sfm_ui_consumer import SfmUiConsumer
from sfmutils.consumer import MqConfig, EXCHANGE

QUEUE = "sfm_ui"
ROUTING_KEYS = ["harvest.status.*", "harvest.status.*.*", "harvest.status.*.*.*", "warc_created",
                "export.status.*", "export.status.*.*"]


class Command(BaseCommand):
    help = 'Starts the message consumer'

    def handle(self, *args, **options):
        username = settings.RABBITMQ_USER
        password = settings.RABBITMQ_PASSWORD
        consumer = SfmUiConsumer(mq_config=MqConfig(settings.RABBITMQ_HOST,
                                 username, password, EXCHANGE,
                                 {QUEUE: ROUTING_KEYS}))
        consumer.run()
