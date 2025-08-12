from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import INET
from datetime import datetime

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 사용자 정보
    user_id = Column(String(50), index=True)
    user_type = Column(String(20))  # physician, admin, system
    user_name = Column(String(100))
    
    # 액션 정보
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100))
    
    # 상세 정보
    details = Column(JSON)
    old_values = Column(JSON)
    new_values = Column(JSON)
    
    # 네트워크 정보
    ip_address = Column(INET)
    user_agent = Column(Text)
    session_id = Column(String(100))
    
    # 시간 정보
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 보안 정보
    success = Column(Boolean, default=True)
    risk_level = Column(String(20), default="low")  # low, medium, high, critical
    
    def __repr__(self):
        return f"<AuditLog(user={self.user_id}, action={self.action}, resource={self.resource_type})>"


# backend/app/models/system.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime

from app.core.database import Base


class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String(100), unique=True, nullable=False, index=True)
    setting_value = Column(Text)
    setting_type = Column(String(20), default="string")  # string, integer, float, boolean, json
    category = Column(String(50), default="general")
    description = Column(Text)
    is_encrypted = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(50))
    
    def __repr__(self):
        return f"<SystemSettings(key={self.setting_key}, value={self.setting_value})>"