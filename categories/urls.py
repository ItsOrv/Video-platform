from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.categories_list, name='list'),
    path('<slug:slug>/', views.category_detail, name='detail'),
]

