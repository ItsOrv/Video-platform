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

def sign_in_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'sign_in.html')

def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                from accounts.models import CustomUser
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully! Please sign in.')
                return redirect('sign_in')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
    return render(request, 'sign_up.html')