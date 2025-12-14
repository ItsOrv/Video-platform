from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import VideoView, UserEngagement, VideoAnalytics, PlatformAnalytics
from videos.models import Video


@login_required
def user_analytics(request):
    """User's personal analytics dashboard"""
    user = request.user
    
    # Get user engagement metrics
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    recent_engagement = UserEngagement.objects.filter(
        user=user,
        date__gte=week_ago
    ).aggregate(
        total_watch_time=Sum('watch_time_minutes'),
        total_videos=Sum('videos_watched')
    )
    
    # Get user's video analytics if they're a creator
    user_videos = Video.objects.filter(uploaded_by=user)
    video_stats = user_videos.aggregate(
        total_views=Sum('views_count'),
        total_videos=Count('id'),
        avg_views=Avg('views_count')
    )
    
    context = {
        'recent_engagement': recent_engagement,
        'video_stats': video_stats,
        'user_videos': user_videos[:10],
    }
    return render(request, 'analytics/user_analytics.html', context)


@login_required
def video_analytics_detail(request, video_id):
    """Detailed analytics for a specific video"""
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)
    
    # Get or create analytics
    analytics, created = VideoAnalytics.objects.get_or_create(video=video)
    
    # Get recent views
    recent_views = VideoView.objects.filter(video=video).order_by('-viewed_at')[:50]
    
    # Calculate completion rate
    total_views = VideoView.objects.filter(video=video).count()
    completed_views = VideoView.objects.filter(video=video, completed=True).count()
    completion_rate = (completed_views / total_views * 100) if total_views > 0 else 0
    
    context = {
        'video': video,
        'analytics': analytics,
        'recent_views': recent_views,
        'completion_rate': completion_rate,
    }
    return render(request, 'analytics/video_analytics.html', context)


@user_passes_test(lambda u: u.is_staff)
def platform_analytics(request):
    """Platform-wide analytics (staff only)"""
    today = timezone.now().date()
    
    # Get or create today's analytics
    platform_stats, created = PlatformAnalytics.objects.get_or_create(date=today)
    
    # Get recent platform stats
    recent_stats = PlatformAnalytics.objects.order_by('-date')[:30]
    
    # Calculate growth metrics
    yesterday = today - timedelta(days=1)
    yesterday_stats = PlatformAnalytics.objects.filter(date=yesterday).first()
    
    context = {
        'platform_stats': platform_stats,
        'recent_stats': recent_stats,
        'yesterday_stats': yesterday_stats,
    }
    return render(request, 'analytics/platform_analytics.html', context)

