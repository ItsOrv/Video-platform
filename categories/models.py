from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Category model - moved from videos app"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-folder')
    color = models.CharField(max_length=50, default='from-indigo-500 to-purple-500')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_video_count(self):
        """Get count of active videos in this category"""
        return self.videos.filter(is_active=True).count()

