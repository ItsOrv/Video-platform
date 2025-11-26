from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from videos import views as video_views
from accounts import views as account_views

# ----------------------------------
# Main URL Patterns
# ----------------------------------

urlpatterns = [
    # Home Page
    path('', video_views.index, name='home'),  # مسیر صفحه اصلی برای نمایش `index.html`

    # Admin Panel
    path('admin/', admin.site.urls),  # مسیر پنل مدیریت

    # User Accounts
    path('accounts/', include('accounts.urls')),  # مسیر مدیریت کاربران و احراز هویت

    # Payments and Subscriptions
    path('payments/', include('payments.urls')),  # مسیر پرداخت‌ها و اشتراک‌ها

    # Videos
    path('videos/', include('videos.urls')),  # مسیر مدیریت ویدیوها و صفحات مرتبط
    path('browse/', video_views.browse, name='browse'),
    path('trending/', video_views.trending, name='trending'),
    path('live/', video_views.live, name='live'),

    # Categories
    path('categories/', include('categories.urls')),  # مسیر دسته‌بندی ویدیوها

    # Tags
    path('tags/', include('tags.urls')),  # مسیر برچسب‌ها

    # Moderation and Reports
    path('moderation/', include('moderation.urls')),  # مسیر مدیریت گزارش‌ها و نظارت

    # Analytics
    path('analytics/', include('analytics.urls')),  # مسیر نمایش آمار و تحلیل‌ها
    
    # Additional pages
    path('sign-in/', account_views.sign_in_view, name='sign_in'),
    path('sign-up/', account_views.sign_up_view, name='sign_up'),
    path('get-started/', video_views.get_started, name='get_started'),
    path('profile/', video_views.user_profile, name='profile'),
    path('watch-history/', video_views.watch_history_page, name='watch_history'),
    path('playlists/', video_views.playlists_page, name='playlists'),
    path('playlists/<int:playlist_id>/', video_views.playlist_detail, name='playlist_detail'),
    path('search/', video_views.search_page, name='search'),
    
    # Footer pages
    path('about/', video_views.about_page, name='about'),
    path('contact/', video_views.contact_page, name='contact'),
    path('privacy/', video_views.privacy_page, name='privacy'),
    path('terms/', video_views.terms_page, name='terms'),
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
