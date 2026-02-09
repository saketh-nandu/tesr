"""
Sentinel AI - Celery Worker Configuration
Async task processing for audio and video analysis.
"""
from celery import Celery

from app.config import settings


# Create Celery app
celery_app = Celery(
    "sentinel",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minute timeout
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)
