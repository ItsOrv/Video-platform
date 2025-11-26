from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default='free')
    subscription_expiry = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"
    
    def is_subscription_active(self):
        """Check if subscription is currently active"""
        if self.subscription_type == 'free':
            return False
        if self.subscription_expiry:
            return self.subscription_expiry >= timezone.now().date()
        return False


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a new user is created"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    
    def has_paid_for_video(self, video):
        """Check if user has paid for a specific video"""
        if not video.is_premium:
            return True
        
        # Check if user has active subscription
        if hasattr(self, 'profile'):
            profile = self.profile
            if profile.subscription_type in ['monthly', 'yearly']:
                if profile.subscription_expiry and profile.subscription_expiry >= timezone.now().date():
                    return True
        
        # Check if user has made a payment for this specific video
        from payments.models import Payment, VideoPurchase
        if hasattr(self, 'video_purchases'):
            return VideoPurchase.objects.filter(user=self, video=video, payment__success=True).exists()
        
        return False
    
    def has_active_subscription(self):
        """Check if user has an active subscription"""
        if hasattr(self, 'profile'):
            profile = self.profile
            if profile.subscription_type in ['monthly', 'yearly']:
                if profile.subscription_expiry and profile.subscription_expiry >= timezone.now().date():
                    return True
        return False