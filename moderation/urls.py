from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('report/', views.report_content, name='report'),
    path('dashboard/', views.moderation_dashboard, name='dashboard'),
    path('report/<int:report_id>/review/', views.review_report, name='review_report'),
]
