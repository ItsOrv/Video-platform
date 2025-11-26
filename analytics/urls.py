from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.user_analytics, name='user_analytics'),
    path('video/<int:video_id>/', views.video_analytics_detail, name='video_analytics'),
    path('platform/', views.platform_analytics, name='platform_analytics'),
]
