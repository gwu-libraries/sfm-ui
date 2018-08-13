from django.core.management.base import BaseCommand, CommandError
from ui.models import CollectionSet
from ui.serialize import RecordSerializer


class Command(BaseCommand):
    help = 'Serializes a collection set so that it can be moved.'

    def add_arguments(self, parser):
        parser.add_argument("collection_set_id",
                            help="The collection set id. Unique fragments of a collection set id will be matched.")
        parser.add_argument("--force", action="store_true",
                            help="Serialize even if collection set has changed since last serialization.")

    def handle(self, *args, **options):
        collection_sets = list(
            CollectionSet.objects.filter(collection_set_id__istartswith=options["collection_set_id"]))
        if len(collection_sets) == 0:
            raise CommandError("Collection set id fragment does not match any collection set ids.")
        if len(collection_sets) > 1:
            raise CommandError("Collection set id fragment matches multiple collection set ids.")
        self.stdout.write("Serializing")
        serializer = RecordSerializer()
        serializer.serialize_collection_set(collection_sets[0], force_serialize=options["force"])
        self.stdout.write("Done serializing")
