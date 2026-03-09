from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'chat_id', 'linkedin_status', 'instagram_status', 'twitter_status', 'created_at')
    search_fields = ('content', 'chat_id')
    list_filter = ('linkedin_status', 'instagram_status', 'twitter_status')
