from django.core.management.base import BaseCommand
from ui.notifications import send_free_space_emails


class Command(BaseCommand):
    help = 'Sends free space warning emails to superusers.'

    def handle(self, *args, **options):
        send_free_space_emails()
