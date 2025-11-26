from django.contrib import admin
from .models import VideoView, UserEngagement, VideoAnalytics, PlatformAnalytics


@admin.register(VideoView)
class VideoViewAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'viewed_at', 'watch_duration', 'completed')
    list_filter = ('completed', 'viewed_at')
    search_fields = ('video__title', 'user__username', 'ip_address')
    readonly_fields = ('viewed_at',)
    date_hierarchy = 'viewed_at'


@admin.register(UserEngagement)
class UserEngagementAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'videos_watched', 'watch_time_minutes', 'likes_given', 'comments_made')
    list_filter = ('date',)
    search_fields = ('user__username',)
    date_hierarchy = 'date'


@admin.register(VideoAnalytics)
class VideoAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('video', 'total_views', 'unique_viewers', 'average_watch_time', 'completion_rate', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('video__title',)
    readonly_fields = ('last_updated',)


@admin.register(PlatformAnalytics)
class PlatformAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_users', 'active_users', 'total_videos', 'total_views', 'revenue')
    list_filter = ('date',)
    readonly_fields = ('date',)
    date_hierarchy = 'date'

