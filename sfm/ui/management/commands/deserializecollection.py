from django.core.management.base import BaseCommand, CommandError
from ui.serialize import RecordDeserializer


class Command(BaseCommand):
    help = 'Deserializes (imports) a collection.'

    def add_arguments(self, parser):
        parser.add_argument("collection_path",
                            help="The path of the collection to be imported. The path should be a subdirectory of "
                                 "a collection set within /sfm-collection-set-data/collection_set")

    def handle(self, *args, **options):
        if not options["collection_path"].startswith("/sfm-collection-set-data/collection_set"):
            raise CommandError("Collection path should be a subdirectory of a collection set within "
                               "/sfm-collection-set-data/collection_set")
        self.stdout.write("Deserializing")
        serializer = RecordDeserializer()
        serializer.deserialize_collection(options["collection_path"])
        self.stdout.write("Done deserializing")
