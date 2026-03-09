"""
bot_app/management/commands/run_bot.py

Django management command to run the Telegram bot.
Usage:
    python manage.py run_bot
"""

from django.core.management.base import BaseCommand
from bot_app.telegram_bot import run_bot


class Command(BaseCommand):
    help = "Start the SocialSync AI Telegram bot"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🤖 Starting SocialSync AI Telegram Bot..."))
        run_bot()
