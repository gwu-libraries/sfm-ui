from django.core.management.base import BaseCommand, CommandError
from ui.models import Warc
from ui.rabbit import RabbitWorker
import json


class Command(BaseCommand):
    help = 'Resends warc_created messages to the messaging service.'

    def add_arguments(self, parser):
        parser.add_argument("routing_key", help="The name of the routing key. May not be warc_created.")
        parser.add_argument("--collection-set", help="Limit to collection set with this collection set id.")
        parser.add_argument("--collection", help="Limit to collection with this collection id.")
        parser.add_argument("--harvest-type", help="Limit to this harvest_type.")
        parser.add_argument("--test", action="store_true", help="Print out the messages instead of sending")

    def handle(self, *args, **options):
        if options["routing_key"] == "warc_created":
            raise CommandError("Cannot send messages to warc_created since they may have unintended consequeunces.")

        warcs = Warc.objects.all()
        if options["collection_set"]:
            warcs = warcs.filter(harvest__collection__collection_set__collection_set_id=options["collection_set"])
        if options["collection"]:
            warcs = warcs.filter(harvest__collection__collection_id=options["collection"])
        if options["harvest_type"]:
            warcs = warcs.filter(harvest__harvest_type=options["harvest_type"])

        if options["test"]:
            for msg in self.message_generator(warcs):
                self.stdout.write(json.dumps(msg))
        else:
            RabbitWorker().send_messages(self.message_generator(warcs), options["routing_key"])
            self.stdout.write("Messages sent")

    @staticmethod
    def message_generator(warcs):
        for warc in warcs:
            yield {
                "warc": {
                    "path": warc.path,
                    "sha1": warc.sha1,
                    "bytes": warc.bytes,
                    "id": warc.warc_id,
                    "date_created": warc.date_created.isoformat()
                },
                "collection_set": {
                    "id": warc.harvest.collection.collection_set.collection_set_id
                },
                "collection": {
                    "id": warc.harvest.collection.collection_id
                },
                "harvest": {
                    "id": warc.harvest.harvest_id,
                    "type": warc.harvest.harvest_type
                }
            }
