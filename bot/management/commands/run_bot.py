from django.core.management.base import BaseCommand
from bot.services.telegram_api import TelegramBot


class Command(BaseCommand):
    help = 'Запуск телеграм-бота'

    def handle(self, *args, **options):
        bot = TelegramBot()
        bot.run()
