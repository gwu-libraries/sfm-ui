from django.core.management.base import BaseCommand
from ui.models import User
from ui.notifications import send_user_harvest_emails


class Command(BaseCommand):
    # Note that this command is primarily for testing purposes.
    # Emails sent using it will not include next harvest (since there
    # is no scheduler running).
    help = 'Sends user harvest emails.'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?')

    def handle(self, *args, **options):
        users = None
        if options['username']:
            users = [User.objects.get(username=options['username'])]
        send_user_harvest_emails(users)
        self.stdout.write('Sent user harvest emails.')
