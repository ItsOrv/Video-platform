"""
Digital Rights Management utilities for video protection
"""
import os
import hashlib
import hmac
from django.conf import settings
from datetime import datetime, timedelta
import jwt


def generate_video_token(user, video, expires_in=3600):
    """
    Generate a secure token for video access
    """
    secret_key = settings.SECRET_KEY
    
    payload = {
        'user_id': user.id,
        'video_id': video.id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow(),
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def verify_video_token(token):
    """
    Verify a video access token
    """
    try:
        secret_key = settings.SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_signed_url(video, user, expires_in=3600):
    """
    Generate a signed URL for video streaming
    """
    secret_key = settings.SECRET_KEY
    
    # Create signature
    message = f"{video.id}:{user.id}:{expires_in}"
    signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Return signed URL parameters
    return {
        'video_id': video.id,
        'user_id': user.id,
        'expires': expires_in,
        'signature': signature,
    }


def verify_signed_url(video_id, user_id, expires, signature):
    """
    Verify a signed URL
    """
    secret_key = settings.SECRET_KEY
    
    message = f"{video_id}:{user_id}:{expires}"
    expected_signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)


def check_video_access(user, video):
    """
    Check if user has access to a video
    """
    # Free videos are always accessible
    if not video.is_premium:
        return True
    
    # Check subscription
    if user.has_active_subscription():
        return True
    
    # Check if user purchased the video
    if user.has_paid_for_video(video):
        return True
    
    return False


def encrypt_video_key(video_id, user_id):
    """
    Encrypt video decryption key for DRM
    """
    secret_key = settings.SECRET_KEY
    
    # In production, use proper encryption (AES, etc.)
    # This is a simplified example
    key = f"{video_id}:{user_id}:{secret_key}"
    encrypted_key = hashlib.sha256(key.encode()).hexdigest()
    
    return encrypted_key

