from django.core.management.base import BaseCommand
from ui.notifications import send_queue_warn_emails


class Command(BaseCommand):
    help = 'Sends queue message warning emails to superusers.'

    def handle(self, *args, **options):
        send_queue_warn_emails()
