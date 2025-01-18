from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def update_subscription(request, subscription_type):
    profile = request.user.profile
    profile.subscription_type = subscription_type
    # Set subscription_expiry logic here
    profile.save()
    return redirect('profile')




from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def register(request):
    # Logic for user registration
    return render(request, 'accounts/register.html')

def login_view(request):
    # Logic for user login
    return render(request, 'accounts/login.html')

def logout_view(request):
    # Logic for user logout
    logout(request)
    return redirect('accounts:login')

def profile(request):
    # User profile page
    return render(request, 'accounts/profile.html')
