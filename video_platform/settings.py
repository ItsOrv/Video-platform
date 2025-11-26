from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-u1+ng!1m8y0%-ueijwn#6#hm+_(1-ev$e415duh+&qd+8$1770')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',  # برای احراز هویت کاربران
    'accounts',      # اپلیکیشن مدیریت کاربران
    'videos',        # اپلیکیشن مدیریت ویدیوها
    'payments',      # اپلیکیشن مدیریت پرداخت‌ها و اشتراک‌ها
    'categories',    # مدیریت دسته‌بندی‌ها
    'tags',          # برچسب‌ها
    'moderation',    # نظارت و گزارش تخلفات
    'analytics',     # تحلیل و آمارگیری
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'video_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'video_platform.wsgi.application'

# Database configuration (SQLite for development, change for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to your database file
    }
}

# Password validation (strong passwords)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and media files settings
STATIC_URL = '/static/'  # The URL for static files (CSS, JS, etc.)
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional static file directories
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where collected static files go in production

MEDIA_URL = '/media/'  # The URL for user-uploaded files (e.g., videos, images)
MEDIA_ROOT = BASE_DIR / 'media'  # The directory where media files are stored

# User authentication
AUTH_USER_MODEL = 'accounts.CustomUser'  # Custom user model for the project

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings (use a real SMTP service in production)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@orvhub.com')

# Subscription and Payment Settings
PAYMENT_GATEWAY_KEY = os.environ.get('PAYMENT_GATEWAY_KEY', '')
PAYMENT_SIMULATE_SUCCESS = os.environ.get('PAYMENT_SIMULATE_SUCCESS', 'true').lower() == 'true'

# Secure video streaming (for DRM)
VIDEO_STREAMING_SERVER = 'your-video-streaming-server-url'

# Security settings for production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# Custom site domain if needed

SITE_ID = 1


CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
