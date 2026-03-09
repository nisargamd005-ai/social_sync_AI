"""
bot_app/telegram_bot.py

Telegram Bot receiver for SocialSync AI.
Receives messages from Telegram, saves them as Post objects,
and triggers the Celery publish_post task asynchronously.

Run standalone:
    python manage.py shell
    from bot_app.telegram_bot import run_bot
    run_bot()

Or as a management command (recommended for production):
    python manage.py run_bot
"""

import os
import django

# Bootstrap Django when running this file directly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from bot_app.models import Post
from bot_app.tasks import publish_post

# ─── Replace with your actual BotFather token ───────────────────────────────
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
# ─────────────────────────────────────────────────────────────────────────────


# ── Handlers ──────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user and explain available commands."""
    await update.message.reply_text(
        "👋 Welcome to *SocialSync AI Bot!*\n\n"
        "Send me any text and I'll post it to all your social media platforms automatically.\n\n"
        "Commands:\n"
        "• /start — Show this help message\n"
        "• /status — Check last post status\n"
        "\nJust type your content and hit send! 🚀",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Receive a text message → save Post → trigger Celery task.
    """
    text = update.message.text.strip()

    if not text:
        await update.message.reply_text("⚠️ Empty message received. Please send some content.")
        return

    # Save to Django DB
    post = Post.objects.create(content=text, chat_id=update.message.chat_id)
    print(f"[TelegramBot] New post created: id={post.id}, chat_id={post.chat_id}, content={text[:60]}")

    # Fire async Celery task
    publish_post.delay(post.id)

    await update.message.reply_text(
        f"✅ *Post received and queued!*\n\n"
        f"📝 Content: _{text[:60]}{'...' if len(text) > 60 else ''}_\n"
        f"🆔 Post ID: `{post.id}`\n\n"
        f"Your post is being published to LinkedIn, Instagram, and Twitter now. 🚀",
        parse_mode="Markdown",
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the status of the most recent post."""
    latest = Post.objects.order_by('-created_at').first()

    if not latest:
        await update.message.reply_text("📭 No posts found yet. Send a message to create one!")
        return

    status_lines = [
        f"📊 *Latest Post Status* (ID: `{latest.id}`)",
        f"",
        f"📝 Content: _{latest.content[:60]}{'...' if len(latest.content) > 60 else ''}_",
        f"",
        f"{'✅' if latest.linkedin_status else '⏳'} LinkedIn: {'Posted' if latest.linkedin_status else 'Pending'}",
        f"{'✅' if latest.instagram_status else '⏳'} Instagram: {'Posted' if latest.instagram_status else 'Pending'}",
        f"{'✅' if latest.twitter_status else '⏳'} Twitter: {'Posted' if latest.twitter_status else 'Pending'}",
        f"",
        f"🕒 Created: {latest.created_at.strftime('%Y-%m-%d %H:%M UTC')}",
    ]

    if latest.error_message:
        status_lines.append(f"\n⚠️ Errors: `{latest.error_message}`")

    await update.message.reply_text("\n".join(status_lines), parse_mode="Markdown")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify user."""
    print(f"[TelegramBot] Error: {context.error}")


# ── Bot runner ────────────────────────────────────────────────────────────────

def run_bot():
    """Build and start the Telegram bot (long-polling)."""
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("❌ ERROR: Please set your TELEGRAM_BOT_TOKEN environment variable or update BOT_TOKEN in telegram_bot.py")
        return

    print("🤖 SocialSync AI Bot is starting...")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    print("✅ Bot is running. Press Ctrl+C to stop.")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    run_bot()
