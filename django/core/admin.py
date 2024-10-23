import traceback
from typing import Any
from django.contrib import admin, messages
from django.contrib.auth.admin import csrf_protect_m
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html
from core.models import Video, Tag

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published', 'num_likes', 'num_views', 'redirect_to_upload', )
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:id>/upload-video/', self.admin_site.admin_view(self.upload_video_view), name='core_video_upload'),
        ]
        return custom_urls + urls
    
    def redirect_to_upload(self, obj: Video):
        url = reverse('admin:core_video_upload', args=[obj.id])
        return format_html(f'<a href="{url}">Upload</a>')

    redirect_to_upload.short_description = 'Upload'
    def upload_video_view(self, request, id):
        return render(request, 'admin/core/upload_video.html')



admin.site.register(Video, VideoAdmin)
admin.site.register(Tag)