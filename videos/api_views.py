from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from datetime import datetime, timedelta
from .models import Video, VideoLike, VideoFavorite, Comment, CommentLike, WatchHistory, Playlist, PlaylistVideo
from .serializers import VideoSerializer
import json

class VideoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        videos = Video.objects.filter(is_active=True)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


class VideoLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        is_like = request.data.get('is_like', True)
        
        like, created = VideoLike.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'is_like': is_like}
        )
        
        if not created:
            if like.is_like == is_like:
                # User clicked same button, remove like/dislike
                like.delete()
                return Response({
                    'likes_count': video.get_likes_count(),
                    'dislikes_count': video.get_dislikes_count(),
                    'user_liked': None,
                    'user_disliked': None
                })
            else:
                # User changed from like to dislike or vice versa
                like.is_like = is_like
                like.save()
        
        return Response({
            'likes_count': video.get_likes_count(),
            'dislikes_count': video.get_dislikes_count(),
            'user_liked': is_like if is_like else None,
            'user_disliked': not is_like if not is_like else None
        })


class VideoFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        favorite, created = VideoFavorite.objects.get_or_create(
            user=request.user,
            video=video
        )
        
        if not created:
            favorite.delete()
            return Response({'is_favorite': False})
        
        return Response({'is_favorite': True})


class CommentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        comments = Comment.objects.filter(video=video, parent=None).order_by('-created_at')
        
        comments_data = []
        for comment in comments:
            # Get replies for this comment
            replies = Comment.objects.filter(parent=comment).order_by('created_at')
            replies_data = []
            for reply in replies:
                replies_data.append({
                    'id': reply.id,
                    'user': reply.user.username,
                    'content': reply.content,
                    'created_at': reply.created_at.isoformat(),
                    'likes_count': reply.get_likes_count(),
                    'is_edited': reply.is_edited,
                })
            
            comments_data.append({
                'id': comment.id,
                'user': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
                'likes_count': comment.get_likes_count(),
                'replies_count': comment.get_replies_count(),
                'is_edited': comment.is_edited,
                'replies': replies_data,
            })
        
        return Response(comments_data)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        content = request.data.get('content', '').strip()
        parent_id = request.data.get('parent_id')
        
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id, video=video)
            except Comment.DoesNotExist:
                pass
        
        comment = Comment.objects.create(
            video=video,
            user=request.user,
            content=content,
            parent=parent
        )
        
        return Response({
            'id': comment.id,
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
        }, status=status.HTTP_201_CREATED)


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        like, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment=comment
        )
        
        if not created:
            like.delete()
            return Response({'likes_count': comment.get_likes_count(), 'is_liked': False})
        
        return Response({'likes_count': comment.get_likes_count(), 'is_liked': True})


class WatchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        watch_duration = request.data.get('watch_duration', 0)
        watch_position = request.data.get('watch_position', 0)
        completed = request.data.get('completed', False)
        
        history, created = WatchHistory.objects.get_or_create(
            user=request.user,
            video=video
        )
        
        history.watch_duration = watch_duration
        history.watch_position = watch_position
        history.completed = completed
        history.save()
        
        return Response({'success': True})


class VideoSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '').strip()
        category = request.GET.get('category')
        sort = request.GET.get('sort', 'relevance')
        
        videos = Video.objects.filter(is_active=True)
        
        if query:
            videos = videos.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        
        if category:
            videos = videos.filter(category__slug=category)
        
        # Premium/Free filter
        premium = request.GET.get('premium') == 'true'
        free = request.GET.get('free') == 'true'
        if premium:
            videos = videos.filter(is_premium=True)
        if free:
            videos = videos.filter(is_premium=False)
        
        # Duration filter
        duration = request.GET.get('duration')
        if duration == 'short':
            videos = videos.filter(duration__lt=300)  # < 5 minutes
        elif duration == 'medium':
            videos = videos.filter(duration__gte=300, duration__lte=1200)  # 5-20 minutes
        elif duration == 'long':
            videos = videos.filter(duration__gt=1200)  # > 20 minutes
        
        # Date filter
        date_filter = request.GET.get('date')
        if date_filter == 'today':
            videos = videos.filter(uploaded_at__date=datetime.now().date())
        elif date_filter == 'week':
            videos = videos.filter(uploaded_at__gte=datetime.now() - timedelta(days=7))
        elif date_filter == 'month':
            videos = videos.filter(uploaded_at__gte=datetime.now() - timedelta(days=30))
        elif date_filter == 'year':
            videos = videos.filter(uploaded_at__gte=datetime.now() - timedelta(days=365))
        
        if sort == 'date':
            videos = videos.order_by('-uploaded_at')
        elif sort == 'views':
            videos = videos.order_by('-views_count')
        elif sort == 'rating':
            videos = videos.annotate(
                likes_count=Count('likes', filter=Q(likes__is_like=True))
            ).order_by('-likes_count')
        else:  # relevance
            videos = videos.order_by('-views_count', '-uploaded_at')
        
        limit = int(request.GET.get('limit', 50))
        videos_list = list(videos[:limit])
        
        # Serialize manually to include thumbnail URL
        results = []
        for video in videos_list:
            results.append({
                'id': video.id,
                'title': video.title,
                'description': video.description,
                'thumbnail': video.thumbnail.url if video.thumbnail else None,
                'views_count': video.views_count,
                'uploaded_at': video.uploaded_at.isoformat(),
                'is_premium': video.is_premium,
            })
        
        return Response(results)


class PlaylistCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name', '').strip()
        description = request.data.get('description', '').strip()
        is_public = request.data.get('is_public', True)
        
        if not name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        playlist = Playlist.objects.create(
            name=name,
            description=description,
            user=request.user,
            is_public=is_public
        )
        
        return Response({
            'id': playlist.id,
            'name': playlist.name,
        }, status=status.HTTP_201_CREATED)


class PlaylistAddVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        video_id = request.data.get('video_id')
        
        if not video_id:
            return Response({'error': 'video_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        video = get_object_or_404(Video, id=video_id)
        
        playlist_video, created = PlaylistVideo.objects.get_or_create(
            playlist=playlist,
            video=video
        )
        
        if not created:
            return Response({'error': 'Video already in playlist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'success': True})


class PlaylistRemoveVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        video_id = request.data.get('video_id')
        
        if not video_id:
            return Response({'error': 'video_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        PlaylistVideo.objects.filter(playlist=playlist, video_id=video_id).delete()
        
        return Response({'success': True})


class PlaylistUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        
        name = request.data.get('name', '').strip()
        description = request.data.get('description', '').strip()
        is_public = request.data.get('is_public', playlist.is_public)
        
        if name:
            playlist.name = name
        if description is not None:
            playlist.description = description
        playlist.is_public = is_public
        playlist.save()
        
        return Response({
            'id': playlist.id,
            'name': playlist.name,
            'description': playlist.description,
            'is_public': playlist.is_public,
        })


class PlaylistDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        playlist.delete()
        return Response({'success': True})


class PlaylistReorderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        video_orders = request.data.get('video_orders', [])  # List of {video_id: order}
        
        for item in video_orders:
            video_id = item.get('video_id')
            order = item.get('order', 0)
            PlaylistVideo.objects.filter(
                playlist=playlist,
                video_id=video_id
            ).update(order=order)
        
        return Response({'success': True})


class PlaylistDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        # Check if playlist is public or user owns it
        if not playlist.is_public and request.user != playlist.user:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        videos = playlist.playlistvideo_set.all().select_related('video').order_by('order', '-added_at')
        videos_data = []
        for pv in videos:
            videos_data.append({
                'id': pv.video.id,
                'title': pv.video.title,
                'thumbnail': pv.video.thumbnail.url if pv.video.thumbnail else None,
                'duration': pv.video.duration,
                'views_count': pv.video.views_count,
                'order': pv.order,
            })
        
        return Response({
            'id': playlist.id,
            'name': playlist.name,
            'description': playlist.description,
            'is_public': playlist.is_public,
            'user': playlist.user.username,
            'videos': videos_data,
        })


class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        from accounts.models import CustomUser
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        if user_to_follow == request.user:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            follow.delete()
            return Response({'is_following': False})
        
        return Response({'is_following': True})


class UserFollowersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        from accounts.models import CustomUser
        user = get_object_or_404(CustomUser, id=user_id)
        
        followers = UserFollow.objects.filter(following=user).select_related('follower')
        followers_data = [{
            'id': f.follower.id,
            'username': f.follower.username,
            'followed_at': f.created_at.isoformat(),
        } for f in followers]
        
        return Response(followers_data)


class UserFollowingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        from accounts.models import CustomUser
        user = get_object_or_404(CustomUser, id=user_id)
        
        following = UserFollow.objects.filter(follower=user).select_related('following')
        following_data = [{
            'id': f.following.id,
            'username': f.following.username,
            'followed_at': f.created_at.isoformat(),
        } for f in following]
        
        return Response(following_data)
