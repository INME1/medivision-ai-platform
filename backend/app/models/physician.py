from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.core.database import Base

class Physician(Base):
    __tablename__ = "physicians"
    
    id = Column(Integer, primary_key=True, index=True)
    physician_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    specialty = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
