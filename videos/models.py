from django.conf import settings
from django.db import models

from django.conf import settings
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='videos/thumbnails/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # قیمت ویدیو برای ویدیوهای پولی
    is_active = models.BooleanField(default=True)  # برای مشخص کردن وضعیت فعال بودن ویدیو
    is_featured = models.BooleanField(default=False)  # برای ویدیوهایی که برجسته هستند

    def __str__(self):
        return self.title

    def get_payment_link(self):
        # تابعی برای گرفتن لینک پرداخت برای ویدیوهای پولی
        if self.is_premium and self.price > 0:
            return f"payment-page/{self.id}/"  # فرض بر این است که لینک پرداخت در اینجا ایجاد می‌شود.
        return None

    def is_available(self, user):
        """
        بررسی دسترسی به ویدیو برای کاربر. اگر ویدیو پولی است، باید پرداخت شده باشد.
        """
        if self.is_premium:
            # بررسی که آیا کاربر پرداخت کرده است یا نه
            # فرض بر این است که تابعی برای بررسی پرداخت کاربران وجود دارد.
            return user.has_paid_for_video(self)
        return True  # برای ویدیوهای رایگان همیشه True است

    def __str__(self):
        return self.title