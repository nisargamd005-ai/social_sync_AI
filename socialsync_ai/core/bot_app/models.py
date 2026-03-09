
from django.db import models

class Post(models.Model):

    content = models.TextField()

    chat_id = models.CharField(max_length=255, null=True, blank=True)

    linkedin_status = models.BooleanField(default=False)
    instagram_status = models.BooleanField(default=False)
    twitter_status = models.BooleanField(default=False)

    scheduled_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.content[:30]
