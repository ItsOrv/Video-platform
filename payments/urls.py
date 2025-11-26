from django.urls import path
from . import views, webhooks

app_name = 'payments'

urlpatterns = [
    path('video/<int:video_id>/', views.process_video_payment, name='video_payment'),
    path('subscribe/<str:subscription_type>/', views.subscribe, name='subscribe'),
    path('history/', views.payment_history, name='history'),
    path('webhook/', webhooks.payment_webhook, name='webhook'),
]