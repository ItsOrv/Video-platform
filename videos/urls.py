from django.urls import path
from . import views, api_views

app_name = 'videos'

urlpatterns = [
    path('', views.index, name='home'),
    path('browse/', views.browse, name='browse'),
    path('trending/', views.trending, name='trending'),
    path('live/', views.live, name='live'),
    path('<int:video_id>/', views.video_detail, name='video_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('watch-history/', views.watch_history_page, name='watch_history'),
    path('playlists/', views.playlists_page, name='playlists'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('search/', views.search_page, name='search'),
    path('upload/', views.upload_video, name='upload'),
    path('<int:video_id>/edit/', views.edit_video, name='edit'),
    path('<int:video_id>/delete/', views.delete_video, name='delete'),
    
    # API endpoints
    path('api/list/', api_views.VideoListView.as_view(), name='api_video_list'),
    path('api/<int:video_id>/like/', api_views.VideoLikeView.as_view(), name='api_video_like'),
    path('api/<int:video_id>/favorite/', api_views.VideoFavoriteView.as_view(), name='api_video_favorite'),
    path('api/<int:video_id>/comments/', api_views.CommentListView.as_view(), name='api_comment_list'),
    path('api/<int:video_id>/comments/create/', api_views.CommentCreateView.as_view(), name='api_comment_create'),
    path('api/comments/<int:comment_id>/like/', api_views.CommentLikeView.as_view(), name='api_comment_like'),
    path('api/<int:video_id>/watch-history/', api_views.WatchHistoryView.as_view(), name='api_watch_history'),
    path('api/search/', api_views.VideoSearchView.as_view(), name='api_video_search'),
    path('api/playlists/create/', api_views.PlaylistCreateView.as_view(), name='api_playlist_create'),
    path('api/playlists/<int:playlist_id>/', api_views.PlaylistDetailView.as_view(), name='api_playlist_detail'),
    path('api/playlists/<int:playlist_id>/update/', api_views.PlaylistUpdateView.as_view(), name='api_playlist_update'),
    path('api/playlists/<int:playlist_id>/delete/', api_views.PlaylistDeleteView.as_view(), name='api_playlist_delete'),
    path('api/playlists/<int:playlist_id>/add-video/', api_views.PlaylistAddVideoView.as_view(), name='api_playlist_add_video'),
    path('api/playlists/<int:playlist_id>/remove-video/', api_views.PlaylistRemoveVideoView.as_view(), name='api_playlist_remove_video'),
    path('api/playlists/<int:playlist_id>/reorder/', api_views.PlaylistReorderView.as_view(), name='api_playlist_reorder'),
    path('api/users/<int:user_id>/follow/', api_views.UserFollowView.as_view(), name='api_user_follow'),
    path('api/users/<int:user_id>/followers/', api_views.UserFollowersView.as_view(), name='api_user_followers'),
    path('api/users/<int:user_id>/following/', api_views.UserFollowingView.as_view(), name='api_user_following'),
]
