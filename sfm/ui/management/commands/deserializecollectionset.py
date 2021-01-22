from django.core.management.base import BaseCommand, CommandError
from ui.serialize import RecordDeserializer


class Command(BaseCommand):
    help = 'Deserializes (imports) a collection set.'

    def add_arguments(self, parser):
        parser.add_argument("collection_set_path",
                            help="The path of the collection set to be imported. The path should be a subdirectory of "
                                 "/sfm-collection-set-data/collection_set")

    def handle(self, *args, **options):
        if not options["collection_set_path"].startswith("/sfm-collection-set-data/collection_set"):
            raise CommandError("Collection set path should be a subdirectory of /sfm-collection-set-data/collection_set")
        self.stdout.write("Deserializing")
        serializer = RecordDeserializer()
        serializer.deserialize_collection_set(options["collection_set_path"])
        self.stdout.write("Done deserializing")
