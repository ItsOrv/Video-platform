"""
Celery tasks for video processing
"""
from celery import shared_task
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import os
import subprocess
from .models import Video


@shared_task
def process_video(video_id):
    """
    Process uploaded video: extract duration, generate thumbnail
    """
    try:
        video = Video.objects.get(id=video_id)
        
        # Extract video duration using ffprobe
        video_path = video.file.path
        if os.path.exists(video_path):
            try:
                # Get duration using ffprobe
                cmd = [
                    'ffprobe',
                    '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    video_path
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    duration = int(float(result.stdout.strip()))
                    video.duration = duration
                    video.save(update_fields=['duration'])
            except Exception as e:
                print(f"Error extracting duration: {e}")
            
            # Generate thumbnail
            try:
                generate_thumbnail.delay(video_id)
            except:
                pass
        
    except Video.DoesNotExist:
        print(f"Video {video_id} not found")
    except Exception as e:
        print(f"Error processing video {video_id}: {e}")


@shared_task
def generate_thumbnail(video_id):
    """
    Generate thumbnail from video
    """
    try:
        video = Video.objects.get(id=video_id)
        
        if not video.file:
            return
        
        video_path = video.file.path
        
        if not os.path.exists(video_path):
            return
        
        # Generate thumbnail using ffmpeg
        thumbnail_path = video_path.replace('.mp4', '_thumb.jpg')
        
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', '00:00:01',
                '-vframes', '1',
                '-q:v', '2',
                thumbnail_path
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Open and resize thumbnail
            if os.path.exists(thumbnail_path):
                img = Image.open(thumbnail_path)
                img.thumbnail((1280, 720), Image.Resampling.LANCZOS)
                
                # Save to video thumbnail field
                with open(thumbnail_path, 'rb') as f:
                    video.thumbnail.save(
                        f'thumbnails/{video.id}.jpg',
                        ContentFile(f.read()),
                        save=True
                    )
                
                # Clean up temporary file
                os.remove(thumbnail_path)
        except subprocess.CalledProcessError as e:
            print(f"Error generating thumbnail: {e}")
        except Exception as e:
            print(f"Error processing thumbnail: {e}")
    
    except Video.DoesNotExist:
        print(f"Video {video_id} not found")
    except Exception as e:
        print(f"Error in generate_thumbnail: {e}")


@shared_task
def update_video_analytics(video_id):
    """
    Update aggregated analytics for a video
    """
    try:
        from analytics.models import VideoAnalytics, VideoView
        
        video = Video.objects.get(id=video_id)
        
        # Get or create analytics
        analytics, created = VideoAnalytics.objects.get_or_create(video=video)
        
        # Update statistics
        views = VideoView.objects.filter(video=video)
        analytics.total_views = views.count()
        analytics.unique_viewers = views.values('user').distinct().count()
        
        # Calculate average watch time
        from django.db.models import Sum
        total_watch_time = views.aggregate(
            total=Sum('watch_duration')
        )['total'] or 0
        if analytics.total_views > 0:
            analytics.average_watch_time = total_watch_time // analytics.total_views
        
        # Calculate completion rate
        completed_views = views.filter(completed=True).count()
        if analytics.total_views > 0:
            analytics.completion_rate = (completed_views / analytics.total_views) * 100
        
        # Update counts
        analytics.likes_count = video.get_likes_count()
        analytics.dislikes_count = video.get_dislikes_count()
        analytics.comments_count = video.get_comments_count()
        
        analytics.save()
    
    except Video.DoesNotExist:
        print(f"Video {video_id} not found")
    except Exception as e:
        print(f"Error updating analytics: {e}")


@shared_task
def cleanup_old_files():
    """
    Clean up old temporary files and inactive videos
    """
    try:
        # Delete files for videos that have been deleted
        # This is a placeholder - implement based on your needs
        pass
    except Exception as e:
        print(f"Error in cleanup: {e}")


@shared_task
def send_video_notification(video_id, user_ids):
    """
    Send notification to users about new video
    """
    try:
        # Implement notification logic
        # This could send emails, push notifications, etc.
        pass
    except Exception as e:
        print(f"Error sending notifications: {e}")

