from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('free', 'Free'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES, default='free')
    subscription_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # اضافه کردن فیلدهای اضافی (در صورت نیاز)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
