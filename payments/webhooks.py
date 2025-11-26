from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Payment, Subscription, VideoPurchase
from accounts.models import UserProfile
from django.utils import timezone
from datetime import timedelta


@csrf_exempt
@require_POST
def payment_webhook(request):
    """
    Handle payment webhook from payment gateway
    """
    try:
        # Parse webhook payload
        # This is a generic implementation - adapt to your payment gateway
        payload = json.loads(request.body)
        
        transaction_id = payload.get('transaction_id')
        status = payload.get('status')
        amount = payload.get('amount')
        user_id = payload.get('user_id')
        
        if not all([transaction_id, status]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Find payment
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)
        
        # Update payment status
        if status == 'completed':
            payment.success = True
            payment.status = 'completed'
            payment.save()
            
            # Handle subscription payments
            if 'subscription' in payload.get('description', '').lower():
                subscription_type = payload.get('subscription_type', 'monthly')
                profile = payment.user.profile
                profile.subscription_type = subscription_type
                
                if subscription_type == 'monthly':
                    profile.subscription_expiry = timezone.now().date() + timedelta(days=30)
                else:
                    profile.subscription_expiry = timezone.now().date() + timedelta(days=365)
                
                profile.save()
                
                # Create subscription record
                Subscription.objects.get_or_create(
                    user=payment.user,
                    subscription_type=subscription_type,
                    payment=payment,
                    defaults={
                        'end_date': profile.subscription_expiry,
                        'is_active': True
                    }
                )
            
            # Handle video purchase payments
            elif 'video' in payload.get('description', '').lower():
                video_id = payload.get('video_id')
                if video_id:
                    from videos.models import Video
                    try:
                        video = Video.objects.get(id=video_id)
                        VideoPurchase.objects.get_or_create(
                            user=payment.user,
                            video=video,
                            payment=payment
                        )
                    except Video.DoesNotExist:
                        pass
        
        elif status == 'failed':
            payment.success = False
            payment.status = 'failed'
            payment.save()
        
        return JsonResponse({'status': 'success'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
