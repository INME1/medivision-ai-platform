from app.celery import celery_app
import time

@celery_app.task
def process_image_task(image_path: str):
    """이미지 처리 테스트 태스크"""
    # 간단한 처리 시뮬레이션
    time.sleep(2)
    return {
        "status": "completed",
        "image_path": image_path,
        "message": "Image processed successfully"
    }
