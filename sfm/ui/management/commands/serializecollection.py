from django.core.management.base import BaseCommand, CommandError
from ui.models import Collection
from ui.serialize import RecordSerializer


class Command(BaseCommand):
    help = 'Serializes a collection so that it can be moved.'

    def add_arguments(self, parser):
        parser.add_argument("collection_id",
                            help="The collection id. Unique fragments of a collection id will be matched.")
        parser.add_argument("--force", action="store_true",
                            help="Serialize even if collection has changed since last serialization.")

    def handle(self, *args, **options):
        collections = list(Collection.objects.filter(collection_id__istartswith=options["collection_id"]))
        if len(collections) == 0:
            raise CommandError("Collection id fragment does not match any collection ids.")
        if len(collections) > 1:
            raise CommandError("Collection id fragment matches multiple collection ids.")
        self.stdout.write("Serializing")
        serializer = RecordSerializer()
        serializer.serialize_collection(collections[0], force_serialize=options["force"])
        self.stdout.write("Done serializing")
