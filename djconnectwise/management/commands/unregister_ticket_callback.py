from django.core.management.base import BaseCommand
from djconnectwise.callback import CallBackHandler


class Command(BaseCommand):
    help = 'Registers the ticket callback with the target connectwise system.'

    def handle(self, *args, **options):
        handler = CallBackHandler()
        handler.remove_ticket_callback()
        print('Removed ticket callback')