from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from .models import Video, Comment, WatchHistory, Playlist, VideoFavorite, UserFollow
from categories.models import Category
from tags.models import Tag

def index(request):
    # Get featured videos for the homepage
    try:
        featured_videos = list(Video.objects.filter(is_active=True, is_featured=True)[:6])
        trending_videos = list(Video.objects.filter(is_active=True).order_by('-views_count', '-uploaded_at')[:8])
        all_videos = list(Video.objects.filter(is_active=True)[:12])
        
        # Get continue watching for authenticated users
        continue_watching = []
        if request.user.is_authenticated:
            continue_watching = WatchHistory.objects.filter(
                user=request.user,
                completed=False
            ).order_by('-watched_at')[:6]
    except Exception as e:
        featured_videos = []
        trending_videos = []
        all_videos = []
        continue_watching = []
    
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
        'continue_watching': continue_watching,
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

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id, is_active=True)
    
    # Increment view count
    video.views_count += 1
    video.save(update_fields=['views_count'])
    
    # Get comments
    comments = Comment.objects.filter(video=video, parent=None).order_by('-created_at')[:50]
    
    # Get related videos (same category or similar tags)
    related_videos = Video.objects.filter(
        is_active=True
    ).exclude(id=video.id)
    
    if video.category:
        related_videos = related_videos.filter(category=video.category)
    
    if video.tags.exists():
        related_videos = related_videos.filter(tags__in=video.tags.all()).distinct()
    
    related_videos = related_videos[:10]
    
    # Get user's like/dislike status
    user_liked = None
    user_favorited = False
    if request.user.is_authenticated:
        try:
            like = video.likes.get(user=request.user)
            user_liked = like.is_like
        except:
            pass
        user_favorited = video.favorited_by.filter(user=request.user).exists()
    
    context = {
        'video': video,
        'comments': comments,
        'related_videos': related_videos,
        'user_liked': user_liked,
        'user_favorited': user_favorited,
    }
    return render(request, 'video_detail.html', context)

@login_required
def user_profile(request):
    user = request.user
    
    # Get user stats
    uploaded_videos = Video.objects.filter(uploaded_by=user, is_active=True)
    total_views = uploaded_videos.aggregate(total=Sum('views_count'))['total'] or 0
    uploaded_count = uploaded_videos.count()
    
    # Get playlists
    playlists = Playlist.objects.filter(user=user)
    
    # Get favorites
    favorites = VideoFavorite.objects.filter(user=user).select_related('video')[:50]
    
    # Get watch history
    watch_history = WatchHistory.objects.filter(user=user).select_related('video').order_by('-watched_at')[:50]
    
    # Get followers/following counts
    followers_count = UserFollow.objects.filter(following=user).count()
    following_count = UserFollow.objects.filter(follower=user).count()
    
    context = {
        'user': user,
        'uploaded_videos': uploaded_videos,
        'total_views': total_views,
        'uploaded_count': uploaded_count,
        'playlists': playlists,
        'favorites': favorites,
        'watch_history': watch_history,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'user_profile.html', context)

@login_required
def watch_history_page(request):
    watch_history = WatchHistory.objects.filter(user=request.user).select_related('video').order_by('-watched_at')
    
    context = {
        'watch_history': watch_history,
    }
    return render(request, 'watch_history.html', context)

@login_required
def playlists_page(request):
    playlists = Playlist.objects.filter(user=request.user).prefetch_related('videos')
    
    context = {
        'playlists': playlists,
    }
    return render(request, 'playlists.html', context)

@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    playlist_videos = playlist.playlistvideo_set.all().select_related('video').order_by('order', '-added_at')
    
    context = {
        'playlist': playlist,
        'playlist_videos': playlist_videos,
    }
    return render(request, 'playlist_detail.html', context)

def search_page(request):
    query = request.GET.get('q', '').strip()
    videos = []
    
    if query:
        videos = Video.objects.filter(
            is_active=True
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-uploaded_at')
    
    context = {
        'query': query,
        'videos': videos,
    }
    return render(request, 'search.html', context)

def about_page(request):
    """About Us page"""
    return render(request, 'about.html')

def contact_page(request):
    """Contact page"""
    return render(request, 'contact.html')

def privacy_page(request):
    """Privacy Policy page"""
    return render(request, 'privacy.html')

def terms_page(request):
    """Terms of Service page"""
    return render(request, 'terms.html')


@login_required
def upload_video(request):
    """Upload a new video"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        category_id = request.POST.get('category')
        tags_input = request.POST.get('tags', '')
        is_premium = request.POST.get('is_premium') == 'on'
        price = request.POST.get('price', '0.00')
        is_featured = request.POST.get('is_featured') == 'on'
        
        if not title or not video_file:
            messages.error(request, 'Title and video file are required.')
        else:
            # Validate file size (max 2GB)
            if video_file.size > 2 * 1024 * 1024 * 1024:
                messages.error(request, 'Video file is too large. Maximum size is 2GB.')
            else:
                # Validate file type
                allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
                file_ext = os.path.splitext(video_file.name)[1].lower()
                if file_ext not in allowed_extensions:
                    messages.error(request, f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}')
                else:
                    # Create video
                    video = Video.objects.create(
                        title=title,
                        description=description,
                        file=video_file,
                        thumbnail=thumbnail if thumbnail else None,
                        uploaded_by=request.user,
                        is_premium=is_premium,
                        price=float(price) if price else 0.00,
                        is_featured=is_featured,
                        duration=0,  # Will be updated by celery task
                    )
                    
                    # Set category
                    if category_id:
                        try:
                            category = Category.objects.get(id=category_id)
                            video.category = category
                            video.save()
                        except Category.DoesNotExist:
                            pass
                    
                    # Add tags
                    if tags_input:
                        tag_names = [tag.strip() for tag in tags_input.split(',')]
                        for tag_name in tag_names:
                            if tag_name:
                                tag, created = Tag.objects.get_or_create(
                                    name=tag_name,
                                    defaults={'slug': tag_name.lower().replace(' ', '-')}
                                )
                                video.tags.add(tag)
                    
                    messages.success(request, 'Video uploaded successfully! It will be processed shortly.')
                    return redirect('videos:video_detail', video_id=video.id)
    
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories': categories,
    }
    return render(request, 'videos/upload.html', context)


@login_required
def edit_video(request, video_id):
    """Edit an existing video"""
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)
    
    if request.method == 'POST':
        video.title = request.POST.get('title', video.title).strip()
        video.description = request.POST.get('description', video.description).strip()
        
        # Update thumbnail if provided
        if request.FILES.get('thumbnail'):
            video.thumbnail = request.FILES.get('thumbnail')
        
        # Update category
        category_id = request.POST.get('category')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                video.category = category
            except Category.DoesNotExist:
                pass
        
        # Update tags
        tags_input = request.POST.get('tags', '')
        if tags_input:
            video.tags.clear()
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tag_names:
                if tag_name:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': tag_name.lower().replace(' ', '-')}
                    )
                    video.tags.add(tag)
        
        video.is_premium = request.POST.get('is_premium') == 'on'
        price = request.POST.get('price', '0.00')
        video.price = float(price) if price else 0.00
        video.is_featured = request.POST.get('is_featured') == 'on'
        video.is_active = request.POST.get('is_active') == 'on'
        
        video.save()
        messages.success(request, 'Video updated successfully!')
        return redirect('videos:video_detail', video_id=video.id)
    
    categories = Category.objects.filter(is_active=True)
    video_tags = ', '.join([tag.name for tag in video.tags.all()])
    
    context = {
        'video': video,
        'categories': categories,
        'video_tags': video_tags,
    }
    return render(request, 'videos/edit.html', context)


@login_required
def delete_video(request, video_id):
    """Delete a video"""
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)
    
    if request.method == 'POST':
        # Delete video file and thumbnail
        if video.file:
            video.file.delete()
        if video.thumbnail:
            video.thumbnail.delete()
        
        video.delete()
        messages.success(request, 'Video deleted successfully!')
        return redirect('profile')
    
    context = {
        'video': video,
    }
    return render(request, 'videos/delete.html', context)
