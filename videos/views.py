from django.shortcuts import render
from .models import Video

def index(request):
    # Get featured videos for the homepage
    try:
        featured_videos = list(Video.objects.filter(is_active=True, is_featured=True)[:6])
        trending_videos = list(Video.objects.filter(is_active=True).order_by('-uploaded_at')[:8])
        all_videos = list(Video.objects.filter(is_active=True)[:12])
    except Exception as e:
        featured_videos = []
        trending_videos = []
        all_videos = []
    
    # Create default categories if none exist
    categories = [
        {'name': 'Action', 'icon': 'fas fa-fire', 'video_count': 0, 'color': 'from-red-500 to-orange-500'},
        {'name': 'Comedy', 'icon': 'fas fa-laugh', 'video_count': 0, 'color': 'from-yellow-500 to-amber-500'},
        {'name': 'Drama', 'icon': 'fas fa-theater-masks', 'video_count': 0, 'color': 'from-purple-500 to-pink-500'},
        {'name': 'Documentary', 'icon': 'fas fa-film', 'video_count': 0, 'color': 'from-blue-500 to-cyan-500'},
        {'name': 'Horror', 'icon': 'fas fa-ghost', 'video_count': 0, 'color': 'from-gray-700 to-gray-900'},
        {'name': 'Sci-Fi', 'icon': 'fas fa-rocket', 'video_count': 0, 'color': 'from-indigo-500 to-purple-500'},
        {'name': 'Romance', 'icon': 'fas fa-heart', 'video_count': 0, 'color': 'from-pink-500 to-rose-500'},
        {'name': 'Thriller', 'icon': 'fas fa-exclamation-triangle', 'video_count': 0, 'color': 'from-red-600 to-red-800'},
    ]
    
    # Create default premium plans
    premium_plans = [
        {
            'name': 'Basic',
            'price': 9.99,
            'features': ['HD Quality', 'Ad-free viewing', 'Mobile access'],
            'recommended': False
        },
        {
            'name': 'Premium',
            'price': 19.99,
            'features': ['4K Quality', 'Ad-free viewing', 'All devices', 'Exclusive content'],
            'recommended': True
        },
        {
            'name': 'Ultimate',
            'price': 29.99,
            'features': ['4K Quality', 'Ad-free viewing', 'All devices', 'Exclusive content', 'Live events'],
            'recommended': False
        }
    ]
    
    # Live streams data (mock for now)
    live_streams = [
        {
            'title': 'Live Gaming Stream',
            'viewers': 1250,
            'category': 'Gaming',
            'thumbnail': None
        },
        {
            'title': 'Music Concert Live',
            'viewers': 3200,
            'category': 'Music',
            'thumbnail': None
        }
    ]
    
    context = {
        'featured_videos': featured_videos,
        'trending_videos': trending_videos,
        'videos': all_videos,
        'categories': categories,
        'premium_plans': premium_plans,
        'live_streams': live_streams,
    }
    return render(request, 'index.html', context)

def browse(request):
    try:
        videos = Video.objects.filter(is_active=True)[:24]
    except:
        videos = []
    context = {'videos': videos}
    # Use template from main templates directory
    return render(request, 'browse.html', context)

def trending(request):
    try:
        videos = Video.objects.filter(is_active=True).order_by('-uploaded_at')[:24]
    except:
        videos = []
    context = {'videos': videos}
    # Use template from main templates directory
    return render(request, 'trending.html', context)

def live(request):
    # Use template from main templates directory
    return render(request, 'live.html')

def get_started(request):
    return render(request, 'get_started.html')

def handler404(request, exception):
    return render(request, 'index.html', status=404)

def handler500(request):
    return render(request, 'index.html', status=500)
