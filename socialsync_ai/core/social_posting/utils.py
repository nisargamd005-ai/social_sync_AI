"""
social_posting/utils.py

Social media API connectors for SocialSync AI.
"""

import os
import requests

# ─────────────────────────────────────────────
# LinkedIn
# ─────────────────────────────────────────────

def post_to_linkedin(content: str, media_path: str = None) -> dict:
    """
    Post content to LinkedIn via the LinkedIn v2 API.
    """
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    person_id = os.environ.get("LINKEDIN_PERSON_ID")
    
    if not access_token or not person_id:
        print(f"[LinkedIn Mock] 📤 Posting: {content[:80]}...")
        return {"status": "mock_success", "platform": "linkedin"}
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    payload = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    response = requests.post("https://api.linkedin.com/v2/ugcPosts", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


# ─────────────────────────────────────────────
# Instagram
# ─────────────────────────────────────────────

def post_to_instagram(content: str, media_path: str = None) -> dict:
    """
    Post content to Instagram using instagrapi.
    """
    username = os.environ.get("INSTAGRAM_USERNAME")
    password = os.environ.get("INSTAGRAM_PASSWORD")
    
    if not username or not password or not media_path:
        print(f"[Instagram Mock] 📤 Posting: {content[:80]}... Media: {media_path}")
        return {"status": "mock_success", "platform": "instagram"}
    
    from instagrapi import Client
    cl = Client()
    cl.login(username, password)
    
    # Uploading a photo
    media = cl.photo_upload(path=media_path, caption=content)
    return {"status": "success", "platform": "instagram", "media_pk": media.pk}


# ─────────────────────────────────────────────
# YouTube
# ─────────────────────────────────────────────

def post_to_youtube(content: str, media_path: str = None) -> dict:
    """
    Post video to YouTube using google-api-python-client.
    """
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    
    if not client_id or not refresh_token or not media_path:
        print(f"[YouTube Mock] 📤 Posting video: {content[:80]}... Media: {media_path}")
        return {"status": "mock_success", "platform": "youtube"}
    
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )
    
    youtube = build('youtube', 'v3', credentials=credentials)
    
    title = content[:90] + "..." if len(content) > 90 else content
    request_body = {
        'snippet': {
            'title': title,
            'description': content,
            'tags': ['SocialSync', 'Post'],
            'categoryId': '22'  # People & Blogs
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    
    media_file = MediaFileUpload(media_path)
    
    response = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()
    
    return {"status": "success", "platform": "youtube", "video_id": response.get("id")}


# ─────────────────────────────────────────────
# Twitter / X
# ─────────────────────────────────────────────

def post_to_twitter(content: str, media_path: str = None) -> dict:
    """
    Post content to Twitter/X via the Twitter API v2.
    """
    print(f"[Twitter Mock] 📤 Posting: {content[:80]}...")
    return {"status": "mock_success", "platform": "twitter"}
