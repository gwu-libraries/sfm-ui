from django.apps import AppConfig
import pika
import os


class RabbitWorker(AppConfig):
    name = 'ui'
    verbose_name = "ui"
    # Create a connection
    credentials = pika.PlainCredentials(
        username=os.environ['MQ_ENV_RABBITMQ_DEFAULT_USER'],
        password=os.environ['MQ_ENV_RABBITMQ_DEFAULT_PASS'])
    parameters = pika.ConnectionParameters(host='mq', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    # create channel
    channel = connection.channel()

    def ready(self):
        # Declare sfm_exchange
        RabbitWorker.channel.exchange_declare(exchange="sfm_exchange",
                                              type="topic", durable=True)
        # Declare harvester queue
        RabbitWorker.channel.queue_declare(queue="sfm_exchange", durable=True)
        # Bind
        RabbitWorker.channel.queue_bind(exchange="sfm_exchange",
                                        queue="sfm_exchange",
                                        routing_key="sfm_exchange")
        pass  # startup code here
