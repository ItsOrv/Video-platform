from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Payment, Subscription, VideoPurchase
from .services import process_payment
from videos.models import Video


@login_required
def process_video_payment(request, video_id):
    """Process payment for a premium video"""
    video = get_object_or_404(Video, id=video_id, is_premium=True)
    
    if request.user.has_paid_for_video(video):
        messages.info(request, 'You have already purchased this video.')
        return redirect('videos:video_detail', video_id=video_id)
    
    if request.method == 'POST':
        # Process payment
        transaction_id, success = process_payment(request.user, video.price)
        
        if success:
            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                amount=video.price,
                success=True,
                status='completed',
                transaction_id=transaction_id,
                payment_method=request.POST.get('payment_method', 'online'),
                description=f'Purchase of video: {video.title}'
            )
            
            # Create video purchase
            VideoPurchase.objects.create(
                user=request.user,
                video=video,
                payment=payment
            )
            
            messages.success(request, 'Payment successful! You can now watch this video.')
            return redirect('videos:video_detail', video_id=video_id)
        else:
            messages.error(request, 'Payment failed. Please try again.')
    
    context = {
        'video': video,
    }
    return render(request, 'payments/video_payment.html', context)


@login_required
def subscribe(request, subscription_type):
    """Subscribe to a plan"""
    if subscription_type not in ['monthly', 'yearly']:
        messages.error(request, 'Invalid subscription type.')
        return redirect('home')
    
    prices = {
        'monthly': 9.99,
        'yearly': 99.99,
    }
    
    if request.method == 'POST':
        amount = prices[subscription_type]
        transaction_id, success = process_payment(request.user, amount)
        
        if success:
            # Create payment
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                success=True,
                status='completed',
                transaction_id=transaction_id,
                payment_method=request.POST.get('payment_method', 'online'),
                description=f'{subscription_type.capitalize()} subscription'
            )
            
            # Update user profile
            profile = request.user.profile
            profile.subscription_type = subscription_type
            
            # Calculate expiry date
            if subscription_type == 'monthly':
                profile.subscription_expiry = timezone.now().date() + timedelta(days=30)
            else:  # yearly
                profile.subscription_expiry = timezone.now().date() + timedelta(days=365)
            
            profile.save()
            
            # Create subscription record
            Subscription.objects.create(
                user=request.user,
                subscription_type=subscription_type,
                payment=payment,
                end_date=profile.subscription_expiry,
                is_active=True
            )
            
            messages.success(request, f'Successfully subscribed to {subscription_type} plan!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Payment failed. Please try again.')
    
    context = {
        'subscription_type': subscription_type,
        'price': prices[subscription_type],
    }
    return render(request, 'payments/subscribe.html', context)


@login_required
def payment_history(request):
    """View payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-timestamp')
    
    context = {
        'payments': payments,
    }
    return render(request, 'payments/history.html', context)
