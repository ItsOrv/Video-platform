from django.shortcuts import render, get_object_or_404
from .models import Category
from videos.models import Video


def categories_list(request):
    """List all categories"""
    from django.db.models import Count, Q
    from videos.models import Video
    
    categories = Category.objects.filter(is_active=True).annotate(
        video_count=Count('videos', filter=Q(videos__is_active=True))
    ).order_by('order', 'name')
    
    context = {'categories': categories}
    return render(request, 'categories.html', context)


def category_detail(request, slug):
    """Show videos in a specific category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    videos = Video.objects.filter(
        category=category,
        is_active=True
    ).order_by('-uploaded_at')
    
    context = {
        'category': category,
        'videos': videos,
    }
    return render(request, 'categories/detail.html', context)

