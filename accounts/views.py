from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings

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


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='accounts/password_reset_email.html',
            )
            messages.success(request, 'Password reset email has been sent.')
            return redirect('accounts:login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})