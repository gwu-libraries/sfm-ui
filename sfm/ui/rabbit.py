from django.conf import settings
from kombu import Connection, Exchange
from sfmutils.consumer import EXCHANGE
import logging
import json

log = logging.getLogger(__name__)


class RabbitWorker:
    def __init__(self):
        self.exchange = Exchange(name=EXCHANGE,
                                 type="topic",
                                 durable=True)

    @staticmethod
    def get_connection():
        return Connection(transport="librabbitmq",
                          hostname=settings.RABBITMQ_HOST,
                          userid=settings.RABBITMQ_USER,
                          password=settings.RABBITMQ_PASSWORD)

    def declare_exchange(self):
        try:
            with self.get_connection() as connection:
                log.debug("Declaring %s exchange", self.exchange.name)
                self.exchange(connection).declare()
        except Exception:
            log.error("Error connecting to RabbitMQ to declare exchange")

    def send_message(self, message, routing_key):
        with self.get_connection() as connection:
            log.debug("Sending message to %s: %s", routing_key, json.dumps(message, indent=4))
            connection.Producer(exchange=self.exchange).publish(message, routing_key=routing_key)

    def send_messages(self, messages, routing_key):
        with self.get_connection() as connection:
            for message in messages:
                log.debug("Sending message to %s: %s", routing_key, json.dumps(message, indent=4))
                connection.Producer(exchange=self.exchange).publish(message, routing_key=routing_key)
