from django.contrib import admin
from .models import (
    Video, VideoLike, VideoFavorite,
    Comment, CommentLike, WatchHistory, Playlist,
    PlaylistVideo, UserFollow
)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'is_active', 'is_premium', 'is_featured', 'views_count', 'uploaded_at')
    list_filter = ('is_active', 'is_premium', 'is_featured', 'category', 'uploaded_at')
    search_fields = ('title', 'description', 'uploaded_by__username')
    readonly_fields = ('uploaded_at', 'views_count')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'uploaded_by', 'category', 'tags')
        }),
        ('Media', {
            'fields': ('file', 'thumbnail', 'duration')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_premium', 'price', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('views_count', 'uploaded_at')
        }),
    )


@admin.register(VideoLike)
class VideoLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'is_like', 'created_at')
    list_filter = ('is_like', 'created_at')
    search_fields = ('user__username', 'video__title')


@admin.register(VideoFavorite)
class VideoFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'created_at')
    search_fields = ('user__username', 'video__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'parent', 'created_at', 'is_edited')
    list_filter = ('is_edited', 'created_at')
    search_fields = ('user__username', 'video__title', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    search_fields = ('user__username', 'comment__content')


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'watch_position', 'watch_duration', 'completed', 'watched_at')
    list_filter = ('completed', 'watched_at')
    search_fields = ('user__username', 'video__title')
    readonly_fields = ('watched_at',)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'user__username')


@admin.register(PlaylistVideo)
class PlaylistVideoAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'video', 'order', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('playlist__name', 'video__title')


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
