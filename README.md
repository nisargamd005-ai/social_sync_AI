# SocialSync AI 🚀

> **AI-powered social media cross-posting bot** — Send one message on Telegram, publish everywhere automatically.

---

## 🏗️ System Architecture

```
User → Telegram Bot
         ↓
 Save Post to Django DB
         ↓
 Celery Task triggered
         ↓
 Post to LinkedIn / Instagram / Twitter
         ↓
 Update status flags in DB
         ↓
 Admin panel shows results
```

---

## 📁 Project Structure

```
socialsync_ai/
├── venv/                          # Python virtual environment
└── core/                          # Django project root
    ├── manage.py
    ├── requirements.txt
    ├── .env.example               # ← Copy to .env and fill credentials
    │
    ├── core/                      # Django project package
    │   ├── settings.py            # App settings + Celery config
    │   ├── celery.py              # Celery app init
    │   ├── urls.py
    │   └── __init__.py            # Imports celery_app
    │
    ├── bot_app/                   # Telegram bot + task logic
    │   ├── models.py              # Post model
    │   ├── admin.py               # Admin registration
    │   ├── tasks.py               # Celery publish_post task
    │   ├── telegram_bot.py        # Telegram bot handlers
    │   └── management/
    │       └── commands/
    │           └── run_bot.py     # `python manage.py run_bot`
    │
    └── social_posting/            # Social media API connectors
        └── utils.py               # post_to_linkedin / instagram / twitter
```

---

## ⚡ Quick Start

### 1. Activate virtual environment
```powershell
cd socialsync_ai
venv\Scripts\activate
```

### 2. Configure credentials
```powershell
copy core\.env.example core\.env
# Edit core\.env with your real API keys
```

### 3. Run Django development server
```powershell
cd core
python manage.py runserver
# Visit http://127.0.0.1:8000/admin
```

### 4. Start Redis (required for Celery)
```powershell
# Download from https://redis.io and run:
redis-server
```

### 5. Start Celery worker (new terminal)
```powershell
cd socialsync_ai\core
venv\Scripts\activate
celery -A core worker -l info
```

### 6. Start Telegram Bot (new terminal)
```powershell
cd socialsync_ai\core
venv\Scripts\activate
python manage.py run_bot
```

---

## 🔑 API Credentials Needed

| Platform   | Where to Get                                    |
|------------|-------------------------------------------------|
| Telegram   | [@BotFather](https://t.me/BotFather) on Telegram |
| LinkedIn   | [LinkedIn Developer Portal](https://developer.linkedin.com) |
| Instagram  | [Meta for Developers](https://developers.facebook.com) |
| Twitter/X  | [Twitter Developer Portal](https://developer.twitter.com) |

---

## 🗂️ Django Admin Panel

Visit `http://127.0.0.1:8000/admin` to monitor all posts:

| Column              | Description                        |
|---------------------|------------------------------------|
| Content             | The post text                      |
| LinkedIn Status     | ✅ Posted / ⏳ Pending              |
| Instagram Status    | ✅ Posted / ⏳ Pending              |
| Twitter Status      | ✅ Posted / ⏳ Pending              |
| Scheduled Time      | When to publish (optional)         |
| Error Message       | Any API errors logged here         |
| Created At          | Timestamp                          |

---

## 🛠️ Adding Real API Integrations

Open `social_posting/utils.py` and replace the mock functions:

### LinkedIn
Uses the [LinkedIn UGC Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/ugc-post-api)

### Instagram
Uses the [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)

### Twitter / X
Uses [Tweepy](https://www.tweepy.org/) with Twitter API v2

---

## ⭐ Advanced Features (Coming Next)

- **Post Scheduling** — Use `django-celery-beat` for time-based publishing
- **Retry Failed Posts** — Already supported via `@shared_task(max_retries=3)`
- **Media Support** — Add image/video attachment to posts
- **Analytics Dashboard** — Track engagement metrics per platform