from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Report, ContentModeration, BannedUser
from videos.models import Video, Comment


@login_required
def report_content(request):
    """Allow users to report content"""
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        content_type = request.POST.get('content_type')
        content_id = request.POST.get('content_id')
        reason = request.POST.get('reason')
        
        if report_type and content_type and content_id and reason:
            Report.objects.create(
                reported_by=request.user,
                report_type=report_type,
                content_type=content_type,
                content_id=content_id,
                reason=reason
            )
            messages.success(request, 'Report submitted successfully. Thank you for helping keep our platform safe.')
            return redirect('home')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'moderation/report.html')


@user_passes_test(lambda u: u.is_staff)
def moderation_dashboard(request):
    """Moderation dashboard for staff"""
    pending_reports = Report.objects.filter(status='pending').order_by('-created_at')[:50]
    recent_actions = ContentModeration.objects.all().order_by('-created_at')[:20]
    active_bans = BannedUser.objects.filter(is_permanent=True) | BannedUser.objects.filter(expires_at__gt=timezone.now())
    
    context = {
        'pending_reports': pending_reports,
        'recent_actions': recent_actions,
        'active_bans': active_bans,
    }
    return render(request, 'moderation/dashboard.html', context)


@user_passes_test(lambda u: u.is_staff)
def review_report(request, report_id):
    """Review and take action on a report"""
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        review_notes = request.POST.get('review_notes', '')
        
        if action == 'approve':
            # Take action on reported content
            if report.content_type == 'video':
                try:
                    video = Video.objects.get(id=report.content_id)
                    video.is_active = False
                    video.save()
                    
                    ContentModeration.objects.create(
                        moderator=request.user,
                        content_type='video',
                        content_id=report.content_id,
                        action='removed',
                        reason=review_notes
                    )
                except Video.DoesNotExist:
                    messages.error(request, 'Video not found.')
            elif report.content_type == 'comment':
                try:
                    comment = Comment.objects.get(id=report.content_id)
                    comment.delete()
                    
                    ContentModeration.objects.create(
                        moderator=request.user,
                        content_type='comment',
                        content_id=report.content_id,
                        action='removed',
                        reason=review_notes
                    )
                except Comment.DoesNotExist:
                    messages.error(request, 'Comment not found.')
            
            report.status = 'resolved'
            report.reviewed_by = request.user
            report.review_notes = review_notes
            report.reviewed_at = timezone.now()
            report.save()
            
            messages.success(request, 'Report resolved and action taken.')
        elif action == 'dismiss':
            report.status = 'dismissed'
            report.reviewed_by = request.user
            report.review_notes = review_notes
            report.reviewed_at = timezone.now()
            report.save()
            
            messages.success(request, 'Report dismissed.')
        
        return redirect('moderation:dashboard')
    
    # Get the reported content
    content = None
    if report.content_type == 'video':
        try:
            content = Video.objects.get(id=report.content_id)
        except Video.DoesNotExist:
            pass
    elif report.content_type == 'comment':
        try:
            content = Comment.objects.get(id=report.content_id)
        except Comment.DoesNotExist:
            pass
    
    context = {
        'report': report,
        'content': content,
    }
    return render(request, 'moderation/review_report.html', context)

