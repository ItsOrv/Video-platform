from django.conf import settings
from django.db import models
from django.utils import timezone


class Report(models.Model):
    REPORT_TYPES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('violence', 'Violence'),
        ('harassment', 'Harassment'),
        ('copyright', 'Copyright Infringement'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    content_type = models.CharField(max_length=20)  # 'video', 'comment', 'user'
    content_id = models.PositiveIntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reports_reviewed'
    )
    review_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['content_type', 'content_id']),
        ]

    def __str__(self):
        return f"Report #{self.id} - {self.get_report_type_display()}"


class ContentModeration(models.Model):
    """Track moderation actions on content"""
    ACTION_TYPES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged'),
        ('removed', 'Removed'),
        ('restricted', 'Restricted'),
    ]
    
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='moderation_actions')
    content_type = models.CharField(max_length=20)
    content_id = models.PositiveIntegerField()
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_action_display()} - {self.content_type} #{self.content_id}"


class BannedUser(models.Model):
    """Track banned users"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ban_info')
    banned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='bans_issued')
    reason = models.TextField()
    banned_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_permanent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-banned_at']

    def __str__(self):
        return f"Banned: {self.user.username}"
    
    def is_active(self):
        """Check if ban is currently active"""
        if self.is_permanent:
            return True
        if self.expires_at:
            return self.expires_at > timezone.now()
        return True

