from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import Tag
from videos.models import Video


def tags_list(request):
    """List all tags with video counts"""
    tags = Tag.objects.annotate(
        video_count=Count('videos', filter=Q(videos__is_active=True))
    ).order_by('-video_count', 'name')
    
    context = {
        'tags': tags,
    }
    return render(request, 'tags/list.html', context)


def tag_detail(request, slug):
    """Show videos for a specific tag"""
    tag = get_object_or_404(Tag, slug=slug)
    videos = Video.objects.filter(
        tags=tag,
        is_active=True
    ).order_by('-uploaded_at')
    
    context = {
        'tag': tag,
        'videos': videos,
    }
    return render(request, 'tags/detail.html', context)

