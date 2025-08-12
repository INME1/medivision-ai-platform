from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.core.database import Base

class MedicalImage(Base):
    __tablename__ = "medical_images"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"))
    image_id = Column(String(100), unique=True, nullable=False)
    file_path = Column(String(500))
    file_size = Column(Integer)
    processing_status = Column(String(20), default="uploaded")
    upload_time = Column(DateTime, default=datetime.utcnow)
