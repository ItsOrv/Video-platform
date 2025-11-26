from django.conf import settings
from django.db import models
from django.utils import timezone


class VideoView(models.Model):
    """Track individual video views"""
    video = models.ForeignKey('videos.Video', on_delete=models.CASCADE, related_name='analytics_views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='video_views')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    watch_duration = models.PositiveIntegerField(default=0, help_text="Duration watched in seconds")
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['video', '-viewed_at']),
            models.Index(fields=['user', '-viewed_at']),
        ]

    def __str__(self):
        return f"View of {self.video.title} at {self.viewed_at}"


class UserEngagement(models.Model):
    """Track user engagement metrics"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='engagement_metrics')
    date = models.DateField(default=timezone.now)
    videos_watched = models.PositiveIntegerField(default=0)
    watch_time_minutes = models.PositiveIntegerField(default=0)
    likes_given = models.PositiveIntegerField(default=0)
    comments_made = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class VideoAnalytics(models.Model):
    """Aggregated analytics for videos"""
    video = models.OneToOneField('videos.Video', on_delete=models.CASCADE, related_name='analytics')
    total_views = models.PositiveIntegerField(default=0)
    unique_viewers = models.PositiveIntegerField(default=0)
    average_watch_time = models.PositiveIntegerField(default=0, help_text="Average watch time in seconds")
    completion_rate = models.FloatField(default=0.0, help_text="Percentage of viewers who completed the video")
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_views']

    def __str__(self):
        return f"Analytics for {self.video.title}"


class PlatformAnalytics(models.Model):
    """Platform-wide analytics"""
    date = models.DateField(unique=True, default=timezone.now)
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    total_videos = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    total_watch_time_minutes = models.PositiveIntegerField(default=0)
    new_registrations = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Platform Analytics - {self.date}"

