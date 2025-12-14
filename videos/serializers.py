from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for Video model"""
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_list = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'file', 'thumbnail',
            'uploaded_by', 'uploaded_by_username', 'uploaded_at',
            'is_premium', 'price', 'is_active', 'is_featured',
            'views_count', 'duration', 'category', 'category_name',
            'tags', 'tags_list', 'likes_count', 'dislikes_count',
            'comments_count'
        ]
        read_only_fields = ['uploaded_by', 'uploaded_at', 'views_count']
    
    def get_tags_list(self, obj):
        """Return list of tag names"""
        return [tag.name for tag in obj.tags.all()]
    
    def get_likes_count(self, obj):
        """Return likes count"""
        return obj.get_likes_count()
    
    def get_dislikes_count(self, obj):
        """Return dislikes count"""
        return obj.get_dislikes_count()
    
    def get_comments_count(self, obj):
        """Return comments count"""
        return obj.get_comments_count()
