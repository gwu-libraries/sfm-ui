from django.apps import AppConfig
from django.conf import settings
import pika
from sfmutils.consumer import EXCHANGE


class RabbitWorker(AppConfig):
    name = 'ui'
    verbose_name = "ui"
    # Create a connection
    credentials = pika.PlainCredentials(
        username=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host='mq', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    # create channel
    channel = connection.channel()

    def ready(self):
        # Declare sfm_exchange
        RabbitWorker.channel.exchange_declare(exchange=EXCHANGE,
                                              type="topic", durable=True)
