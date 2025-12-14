from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery

# تنظیمات پروژه
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_platform.settings')

app = Celery('video_platform')

# تنظیمات Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# شناسایی خودکار وظایف (tasks)
app.autodiscover_tasks()

logger = logging.getLogger(__name__)

@app.task(bind=True)
def debug_task(self):
    logger.debug(f'Request: {self.request!r}')
