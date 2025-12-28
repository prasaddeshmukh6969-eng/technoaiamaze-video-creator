"""
Antigravity AI - Celery Configuration
Background job queue for video generation
"""
from celery import Celery
from core.config import settings

# Initialize Celery app
celery_app = Celery(
    'antigravity',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['routers.v1_generation']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_time_limit=settings.CELERY_TASK_TIMEOUT,
    task_soft_time_limit=settings.CELERY_TASK_TIMEOUT - 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=10,  # Restart worker after 10 tasks (clear GPU memory)
)
