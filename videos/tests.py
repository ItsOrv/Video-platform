from celery import shared_task

@shared_task
def process_video(video_id):
    # Logic to process video
    pass
