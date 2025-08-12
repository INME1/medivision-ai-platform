from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime

from app.core.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    birth_date = Column(Date)
    gender = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
