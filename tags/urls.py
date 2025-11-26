from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [
    path('', views.tags_list, name='list'),
    path('<slug:slug>/', views.tag_detail, name='detail'),
]
