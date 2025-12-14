from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm


@login_required
def update_subscription(request, subscription_type):
    """Update user subscription"""
    if subscription_type not in ['free', 'monthly', 'yearly']:
        messages.error(request, 'Invalid subscription type.')
        return redirect('accounts:profile')
    
    # Ensure profile exists
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.subscription_type = subscription_type
    
    # Set subscription_expiry logic
    if subscription_type == 'free':
        profile.subscription_expiry = None
    elif subscription_type == 'monthly':
        from django.utils import timezone
        from datetime import timedelta
        if not profile.subscription_expiry or profile.subscription_expiry < timezone.now().date():
            profile.subscription_expiry = timezone.now().date() + timedelta(days=30)
        else:
            profile.subscription_expiry = profile.subscription_expiry + timedelta(days=30)
    elif subscription_type == 'yearly':
        from django.utils import timezone
        from datetime import timedelta
        if not profile.subscription_expiry or profile.subscription_expiry < timezone.now().date():
            profile.subscription_expiry = timezone.now().date() + timedelta(days=365)
        else:
            profile.subscription_expiry = profile.subscription_expiry + timedelta(days=365)
    
    profile.save()
    messages.success(request, f'Subscription updated to {subscription_type}.')
    return redirect('accounts:profile')


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not all([username, email, password]):
            messages.error(request, 'Please fill in all required fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            try:
                from accounts.models import CustomUser
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, 'Account created successfully! Please sign in.')
                return redirect('sign_in')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'accounts/register.html')

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    # Logic for user logout
    logout(request)
    return redirect('accounts:login')

@login_required
def profile(request):
    """User profile page"""
    user = request.user
    # Ensure profile exists
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Update profile
        if profile:
            profile.bio = request.POST.get('bio', profile.bio)
            if request.FILES.get('avatar'):
                profile.avatar = request.FILES.get('avatar')
            profile.save()
        
        # Update user info
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        if hasattr(user, 'phone_number'):
            user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


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