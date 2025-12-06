from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'file', 'sha256', 'status', 'uploaded_at')
    search_fields = ('sha256', 'owner__username')
