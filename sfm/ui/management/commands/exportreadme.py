from __future__ import absolute_import
from django.core.management.base import BaseCommand, CommandError
from ui.export import create_readme_for_collection
from ui.models import Collection


class Command(BaseCommand):
    help = 'Serializes a collection so that it can be moved.'

    def add_arguments(self, parser):
        parser.add_argument("collection_id",
                            help="The collection id. Unique fragments of a collection id will be matched.")

    def handle(self, *args, **options):
        collections = list(Collection.objects.filter(collection_id__istartswith=options["collection_id"]))
        if len(collections) == 0:
            raise CommandError("Collection id fragment does not match any collection ids.")
        if len(collections) > 1:
            raise CommandError("Collection id fragment matches multiple collection ids.")
        self.stdout.write(create_readme_for_collection(collections[0]))
