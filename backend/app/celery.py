from celery import Celery
import os

# Redis URL 설정 (컨테이너 네트워크에서 접근)
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# Celery 앱 생성
celery_app = Celery(
    'medivision',
    broker=redis_url,
    backend=redis_url,
    include=['app.tasks.image_processing']
)

# Celery 설정
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30분
    task_soft_time_limit=60,  # 1분
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# Flower를 위한 설정
celery_app.conf.flower_url_prefix = ''
celery_app.conf.flower_basic_auth = None

if __name__ == '__main__':
    celery_app.start()
