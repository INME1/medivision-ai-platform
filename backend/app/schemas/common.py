from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ProcessingStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    timestamp: datetime = datetime.utcnow()
