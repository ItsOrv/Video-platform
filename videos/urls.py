
from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.index, name='home'),  # مسیر روت سایت برای نمایش index.html
]
