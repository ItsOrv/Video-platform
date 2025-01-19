from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from videos import views

# ----------------------------------
# Main URL Patterns
# ----------------------------------

urlpatterns = [
    # Home Page
    path('', views.index, name='home'),  # مسیر صفحه اصلی برای نمایش `index.html`

    # Admin Panel
    path('admin/', admin.site.urls),  # مسیر پنل مدیریت

    # User Accounts
    path('accounts/', include('accounts.urls')),  # مسیر مدیریت کاربران و احراز هویت

    # Payments and Subscriptions
    path('payments/', include('payments.urls')),  # مسیر پرداخت‌ها و اشتراک‌ها

    # Videos
    path('videos/', include('videos.urls')),  # مسیر مدیریت ویدیوها و صفحات مرتبط

    # Categories
    path('categories/', include('categories.urls')),  # مسیر دسته‌بندی ویدیوها

    # Tags
    path('tags/', include('tags.urls')),  # مسیر برچسب‌ها

    # Moderation and Reports
    path('moderation/', include('moderation.urls')),  # مسیر مدیریت گزارش‌ها و نظارت

    # Analytics
    path('analytics/', include('analytics.urls')),  # مسیر نمایش آمار و تحلیل‌ها
]

# ----------------------------------
# Static and Media Files
# ----------------------------------

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ----------------------------------
# Error Handling (Optional)
# ----------------------------------

handler404 = 'videos.views.handler404'  # نمایش صفحه سفارشی برای خطای 404
handler500 = 'videos.views.handler500'  # نمایش صفحه سفارشی برای خطای 500
