from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "MediVision AI Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    DATABASE_URL: str = "postgresql://mediadmin:secure_password_2025@postgres:5432/medivision"
    REDIS_URL: str = "redis://redis:6379/0"
    
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production-2025"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    MAX_FILE_SIZE: int = 104857600
    ALLOWED_EXTENSIONS: List[str] = ["dcm", "dicom", "jpg", "jpeg", "png"]
    
    model_config = {"env_file": ".env"}

settings = Settings()
