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
    """User registration with input validation"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Input validation and sanitization
        if not all([username, email, password]):
            messages.error(request, 'Please fill in all required fields.')
        elif len(username) < 3 or len(username) > 30:
            messages.error(request, 'Username must be between 3 and 30 characters.')
        elif not username.replace('_', '').replace('-', '').isalnum():
            messages.error(request, 'Username can only contain letters, numbers, hyphens, and underscores.')
        elif '@' not in email or len(email) > 254:
            messages.error(request, 'Please enter a valid email address.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif len(password) > 128:
            messages.error(request, 'Password is too long (maximum 128 characters).')
        else:
            try:
                from accounts.models import CustomUser
                # Check if username or email already exists
                if CustomUser.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists. Please choose another.')
                elif CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered. Please sign in or use a different email.')
                else:
                    user = CustomUser.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    messages.success(request, 'Account created successfully! Please sign in.')
                    return redirect('sign_in')
            except Exception as e:
                # Don't expose internal error details to users
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error creating account: {str(e)}", exc_info=True)
                messages.error(request, 'An error occurred while creating your account. Please try again.')
    
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
    """User profile page with input validation"""
    user = request.user
    # Ensure profile exists
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        # Update profile with validation
        if profile:
            bio = request.POST.get('bio', '').strip()
            # Limit bio length to prevent abuse
            if len(bio) <= 500:
                profile.bio = bio
            else:
                messages.error(request, 'Bio cannot exceed 500 characters.')
                bio = bio[:500]
                profile.bio = bio
            
            # Validate and save avatar if provided
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
                # Check file size (max 5MB)
                if avatar.size > 5 * 1024 * 1024:
                    messages.error(request, 'Avatar file size cannot exceed 5MB.')
                else:
                    # Check file type
                    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
                    if avatar.content_type in allowed_types:
                        profile.avatar = avatar
                    else:
                        messages.error(request, 'Invalid file type. Please upload a JPEG, PNG, GIF, or WebP image.')
            profile.save()
        
        # Update user info with validation
        email = request.POST.get('email', '').strip()
        if email and '@' in email and len(email) <= 254:
            user.email = email
        elif email:
            messages.error(request, 'Please enter a valid email address.')
        
        first_name = request.POST.get('first_name', '').strip()
        if len(first_name) <= 150:
            user.first_name = first_name
        else:
            messages.error(request, 'First name cannot exceed 150 characters.')
        
        last_name = request.POST.get('last_name', '').strip()
        if len(last_name) <= 150:
            user.last_name = last_name
        else:
            messages.error(request, 'Last name cannot exceed 150 characters.')
        
        if hasattr(user, 'phone_number'):
            phone_number = request.POST.get('phone_number', '').strip()
            # Basic phone validation
            if phone_number and len(phone_number) <= 20:
                user.phone_number = phone_number
            elif phone_number:
                messages.error(request, 'Phone number is too long.')
        
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
    """User sign up with input validation"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Input validation and sanitization
        if not all([username, email, password]):
            messages.error(request, 'Please fill in all required fields.')
        elif len(username) < 3 or len(username) > 30:
            messages.error(request, 'Username must be between 3 and 30 characters.')
        elif not username.replace('_', '').replace('-', '').isalnum():
            messages.error(request, 'Username can only contain letters, numbers, hyphens, and underscores.')
        elif '@' not in email or len(email) > 254:
            messages.error(request, 'Please enter a valid email address.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif len(password) > 128:
            messages.error(request, 'Password is too long (maximum 128 characters).')
        else:
            try:
                from accounts.models import CustomUser
                # Check if username or email already exists
                if CustomUser.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists. Please choose another.')
                elif CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Email already registered. Please sign in or use a different email.')
                else:
                    user = CustomUser.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, 'Account created successfully! Please sign in.')
                    return redirect('sign_in')
            except Exception as e:
                # Don't expose internal error details to users
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error creating account: {str(e)}", exc_info=True)
                messages.error(request, 'An error occurred while creating your account. Please try again.')
    return render(request, 'sign_up.html')