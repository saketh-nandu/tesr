"""
Sentinel AI - Celery Tasks
Async tasks for heavy processing operations.
"""
from pathlib import Path

from app.workers.celery_app import celery_app
from app.models.audio_analyzer import get_audio_analyzer
from app.models.video_analyzer import get_video_analyzer
from app.utils.file_handler import delete_file


@celery_app.task(bind=True, max_retries=3)
def analyze_audio_task(self, file_path: str) -> dict:
    """
    Async task for audio analysis.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Analysis results dict
    """
    try:
        analyzer = get_audio_analyzer()
        result = analyzer.analyze(Path(file_path))
        
        # Clean up file after processing
        delete_file(Path(file_path))
        
        return result
    except Exception as e:
        # Retry on failure
        raise self.retry(exc=e, countdown=5)


@celery_app.task(bind=True, max_retries=3)
def analyze_video_task(self, file_path: str) -> dict:
    """
    Async task for video analysis.
    
    Args:
        file_path: Path to the video file
        
    Returns:
        Analysis results dict
    """
    try:
        analyzer = get_video_analyzer()
        result = analyzer.analyze(Path(file_path))
        
        # Clean up file after processing
        delete_file(Path(file_path))
        
        return result
    except Exception as e:
        # Retry on failure
        raise self.retry(exc=e, countdown=5)
