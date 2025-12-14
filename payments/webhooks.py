from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import os
import logging
from .models import Payment, Subscription, VideoPurchase
from accounts.models import UserProfile
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def payment_webhook(request):
    """
    Handle payment webhook from payment gateway
    Includes signature verification for security
    """
    try:
        # SECURITY: Verify webhook signature to prevent unauthorized requests
        webhook_secret = os.environ.get('PAYMENT_WEBHOOK_SECRET')
        if webhook_secret:
            import hmac
            import hashlib
            from django.conf import settings
            
            # Get signature from header (common patterns: X-Signature, X-Webhook-Signature, Signature)
            received_signature = (
                request.headers.get('X-Signature') or 
                request.headers.get('X-Webhook-Signature') or 
                request.headers.get('Signature') or
                ''
            )
            
            if received_signature:
                # Calculate expected signature
                expected_signature = hmac.new(
                    webhook_secret.encode('utf-8'),
                    request.body,
                    hashlib.sha256
                ).hexdigest()
                
                # Use constant-time comparison to prevent timing attacks
                if not hmac.compare_digest(received_signature, expected_signature):
                    logger.warning(f"Invalid webhook signature. IP: {request.META.get('REMOTE_ADDR')}")
                    return JsonResponse({'error': 'Invalid signature'}, status=401)
            else:
                # In production, require signature
                if not settings.DEBUG:
                    logger.warning(f"Missing webhook signature. IP: {request.META.get('REMOTE_ADDR')}")
                    return JsonResponse({'error': 'Missing signature'}, status=401)
        
        # Parse webhook payload
        
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
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
                if subscription_type not in ['monthly', 'yearly']:
                    subscription_type = 'monthly'
                
                # Ensure profile exists
                profile, created = UserProfile.objects.get_or_create(user=payment.user)
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
        # Log error but don't expose details to client
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Internal server error'}, status=500)
