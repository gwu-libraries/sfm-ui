from django.core.management.base import BaseCommand

from ui.models import User
from ui.notifications import send_free_space_emails


class Command(BaseCommand):
    help = 'Sends free space warning emails to superusers.'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?')

    def handle(self, *args, **options):
        users = None
        if options['username']:
            users = [User.objects.get(username=options['username'])]
        send_free_space_emails(users)
