from django.core.management.base import BaseCommand
from ui.models import Harvest


class Command(BaseCommand):
    help = 'Delete web harvests.'

    def add_arguments(self, parser):
        parser.add_argument('collection_id')

    def handle(self, *args, **options):
        for harvest in Harvest.objects.filter(harvest_type='web', collection__collection_id=options['collection_id']):
            self.stdout.write('Deleting {}'.format(harvest.harvest_id))
            harvest.delete()
