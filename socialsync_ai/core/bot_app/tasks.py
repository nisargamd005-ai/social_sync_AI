import os
import asyncio
from celery import shared_task
from telegram import Bot

from .models import Post
from social_posting.utils import post_to_linkedin, post_to_instagram, post_to_twitter, post_to_youtube
from social_posting.ai_agent import analyze_command, prepare_content

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

def send_telegram_notification(chat_id, message):
    if not chat_id:
        print(f"[Telegram Mock] Not sending notification. No chat id provided. Message: {message}")
        return
    
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN" or not BOT_TOKEN:
        print(f"[Telegram Mock] to {chat_id}: {message}")
        return

    try:
        bot = Bot(token=BOT_TOKEN)
        asyncio.run(bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown"))
        print(f"[Telegram Notification] Sent message to {chat_id}")
    except Exception as e:
        print(f"[Telegram Notification Error] Failed to send to {chat_id}: {e}")


@shared_task(bind=True, max_retries=3)
def publish_post(self, post_id):
    """
    Celery task to publish a post specifically requested per social media platform.
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print(f"[publish_post] Post with id={post_id} not found. Skipping.")
        return

    # 4. Analyze Command
    analysis = analyze_command(post.content)
    platforms = analysis.get("platforms", [])
    base_content = analysis.get("base_content", post.content)

    print(f"[publish_post] Analyzed Post ID={post.id} | Platforms to post: {platforms}")

    errors = []
    successes = []

    # 5 & 6 & 7. Prepare Content and Post to Platforms, and Check Success
    
    # --- LinkedIn ---
    if "linkedin" in platforms:
        try:
            content = prepare_content(base_content, "linkedin")
            post_to_linkedin(content, media_path=post.media_path)
            post.linkedin_status = True
            successes.append("LinkedIn")
            print(f"[LinkedIn] ✅ Posted successfully for post_id={post_id}")
        except Exception as e:
            errors.append(f"LinkedIn: {str(e)}")
            print(f"[LinkedIn] ❌ Failed for post_id={post_id}: {e}")

    # --- Instagram ---
    if "instagram" in platforms:
        try:
            content = prepare_content(base_content, "instagram")
            post_to_instagram(content, media_path=post.media_path)
            post.instagram_status = True
            successes.append("Instagram")
            print(f"[Instagram] ✅ Posted successfully for post_id={post_id}")
        except Exception as e:
            errors.append(f"Instagram: {str(e)}")
            print(f"[Instagram] ❌ Failed for post_id={post_id}: {e}")

    # --- YouTube ---
    if "youtube" in platforms:
        try:
            content = prepare_content(base_content, "youtube")
            post_to_youtube(content, media_path=post.media_path)
            post.youtube_status = True
            successes.append("YouTube")
            print(f"[YouTube] ✅ Posted successfully for post_id={post_id}")
        except Exception as e:
            errors.append(f"YouTube: {str(e)}")
            print(f"[YouTube] ❌ Failed for post_id={post_id}: {e}")

    # --- Twitter / X ---
    if "twitter" in platforms:
        try:
            content = prepare_content(base_content, "twitter")
            post_to_twitter(content, media_path=post.media_path)
            post.twitter_status = True
            successes.append("Twitter")
            print(f"[Twitter] ✅ Posted successfully for post_id={post_id}")
        except Exception as e:
            errors.append(f"Twitter: {str(e)}")
            print(f"[Twitter] ❌ Failed for post_id={post_id}: {e}")

    # Save all status changes and error logs
    if errors:
        post.error_message = " | ".join(errors)
    else:
        post.error_message = None

    post.save()

    # 8 & 9. Notification Sent to User
    if errors:
        message = (
            f"⚠️ *Posting Alert for Post ID* `{post.id}`\n\n"
            f"Some platforms encountered errors during posting.\n\n"
            f"✅ *Successful:* {', '.join(successes) if successes else 'None'}\n"
            f"❌ *Failed:* {post.error_message}\n\n"
            f"Please review your message or API credentials."
        )
    else:
        message = (
            f"🎉 *Success! Your post was published!* (ID: `{post.id}`)\n\n"
            f"Platforms posted to: {', '.join(successes)}\n"
        )

    send_telegram_notification(post.chat_id, message)

    print(f"[publish_post] Finished for post_id={post_id}. Errors: {errors or 'None'}")
