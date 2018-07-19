from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Creates or updates a Site.'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)
        parser.add_argument('name')
        parser.add_argument('domain', default='localhost', nargs='?')

    def handle(self, *args, **options):
        try:
            site = Site.objects.get(id=options['id'])
            site.name = options['name']
            site.domain = options['domain']
        except Site.DoesNotExist:
            site = Site.objects.create(id=options['id'], name=options['name'], domain=options['domain'])

        site.save()
        self.stdout.write('Created or updated site {}.'.format(options['id']))
