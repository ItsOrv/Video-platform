from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # User registration page
    path('register/', views.register, name='register'),
    
    # User login page
    path('login/', views.login_view, name='login'),
    
    # User logout
    path('logout/', views.logout_view, name='logout'),
    
    # Password reset
    path('password_reset/', views.password_reset, name='password_reset'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
]
