from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# تنظیمات پروژه
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_platform.settings')

app = Celery('video_platform')

# تنظیمات Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# شناسایی خودکار وظایف (tasks)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
