from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.index, name='home'),  # مسیر روت سایت برای نمایش index.html
    path('browse/', views.browse, name='browse'),
    path('trending/', views.trending, name='trending'),
    path('live/', views.live, name='live'),
]
