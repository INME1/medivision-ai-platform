from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # 기본 애플리케이션 설정
    PROJECT_NAME: str = "MediVision AI Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # 데이터베이스 설정
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Redis 설정
    REDIS_URL: str
    
    # MinIO 설정
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str = "medivision-storage"
    DICOM_BUCKET_NAME: str = "dicom-files"
    PROCESSED_BUCKET_NAME: str = "processed-images"
    
    # JWT 설정
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080"
    ]
    
    # 파일 업로드 설정
    MAX_FILE_SIZE: int = 104857600  # 100MB
    UPLOAD_DIR: str = "./uploads"
    MODEL_DIR: str = "./models"
    ALLOWED_EXTENSIONS: List[str] = ["dcm", "dicom", "jpg", "jpeg", "png"]
    
    # AI 모델 설정
    MODEL_CONFIDENCE_THRESHOLD: float = 0.8
    MAX_PREDICTION_TIME: int = 60  # seconds
    GPU_ENABLED: bool = False
    
    # Celery 설정
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    
    # 보안 설정
    BCRYPT_ROUNDS: int = 12
    SESSION_TIMEOUT: int = 3600  # 1 hour
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 모니터링 설정
    PROMETHEUS_METRICS_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL: int = 30
    
    # DICOM 처리 설정
    DICOM_TEMP_DIR: str = "./uploads/temp"
    DICOM_PROCESSED_DIR: str = "./uploads/processed"
    
    # 의료 데이터 규정 준수
    HIPAA_COMPLIANT: bool = True
    AUDIT_LOG_ENABLED: bool = True
    DATA_RETENTION_DAYS: int = 2555  # 7년
    
    @property
    def database_url_sync(self) -> str:
        """동기 SQLAlchemy 연결용 URL"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql://")
    
    @property
    def database_url_async(self) -> str:
        """비동기 SQLAlchemy 연결용 URL"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()

# 개발/프로덕션 환경별 설정 검증
def validate_settings():
    """설정 유효성 검사"""
    required_fields = [
        "DATABASE_URL",
        "REDIS_URL", 
        "JWT_SECRET_KEY",
        "MINIO_ENDPOINT",
        "MINIO_ACCESS_KEY",
        "MINIO_SECRET_KEY"
    ]
    
    missing_fields = []
    for field in required_fields:
        if not getattr(settings, field, None):
            missing_fields.append(field)
    
    if missing_fields:
        raise ValueError(f"Missing required environment variables: {missing_fields}")
    
    # 프로덕션 환경 추가 검사
    if settings.ENVIRONMENT == "production":
        if settings.DEBUG:
            raise ValueError("DEBUG must be False in production")
        if settings.JWT_SECRET_KEY == "your-super-secret-jwt-key-change-in-production-2025":
            raise ValueError("Change default JWT_SECRET_KEY in production")

# 설정 유효성 검사 실행
validate_settings()