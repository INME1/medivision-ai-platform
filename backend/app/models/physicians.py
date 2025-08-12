from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Physician(Base):
    __tablename__ = "physicians"
    
    id = Column(Integer, primary_key=True, index=True)
    physician_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # 개인 정보
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    
    # 전문 정보
    specialty = Column(String(100))
    sub_specialty = Column(String(100))
    license_number = Column(String(50))
    department = Column(String(100))
    position = Column(String(50))  # 주치의, 전문의, 레지던트 등
    
    # 자격 정보
    medical_school = Column(String(200))
    residency_program = Column(String(200))
    board_certifications = Column(Text)  # JSON 형태
    years_of_experience = Column(Integer)
    
    # 계정 정보
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    
    # 시스템 정보
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    reviews = relationship("PhysicianReview", back_populates="physician")
    diagnostic_reports = relationship("DiagnosticReport", back_populates="physician")
    
    def __repr__(self):
        return f"<Physician(id={self.physician_id}, name={self.name}, specialty={self.specialty})>"


class PhysicianReview(Base):
    __tablename__ = "physician_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("ai_predictions.id"), nullable=False)
    physician_id = Column(String(50), ForeignKey("physicians.physician_id"), nullable=False)
    
    # 검토 결과
    is_correct = Column(Boolean)
    confidence_in_ai = Column(Float)  # AI 결과에 대한 의사의 신뢰도 (0-1)
    
    # 수정 사항
    corrected_diagnosis = Column(String(200))
    corrected_confidence = Column(Float)
    additional_findings = Column(Text)
    
    # 피드백
    feedback = Column(Text)
    improvement_suggestions = Column(Text)
    difficulty_level = Column(Integer)  # 1-5, 진단 난이도
    
    # 시간 정보
    review_time = Column(DateTime, default=datetime.utcnow)
    time_spent_minutes = Column(Integer)  # 검토에 소요된 시간(분)
    
    # 관계 설정
    prediction = relationship("AIPrediction", back_populates="physician_reviews")
    physician = relationship("Physician", back_populates="reviews")
    
    def __repr__(self):
        return f"<PhysicianReview(prediction_id={self.prediction_id}, physician={self.physician_id})>"


# backend/app/models/report.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class DiagnosticReport(Base):
    __tablename__ = "diagnostic_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(String(100), ForeignKey("medical_images.image_id"), nullable=False)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False)
    physician_id = Column(String(50), ForeignKey("physicians.physician_id"), nullable=False)
    
    # 보고서 내용
    title = Column(String(200))
    findings = Column(Text, nullable=False)
    impression = Column(Text, nullable=False)
    recommendations = Column(Text)
    clinical_history = Column(Text)
    technique = Column(Text)
    comparison = Column(Text)
    
    # 진단 정보
    primary_diagnosis = Column(String(200))
    secondary_diagnoses = Column(Text)  # JSON 배열
    icd_codes = Column(Text)  # JSON 배열
    urgency_level = Column(String(20))  # routine, urgent, stat
    
    # 상태 정보
    report_status = Column(String(20), default="draft")  # draft, preliminary, final, amended
    is_critical = Column(Boolean, default=False)
    requires_followup = Column(Boolean, default=False)
    followup_instructions = Column(Text)
    
    # 시간 정보
    created_at = Column(DateTime, default=datetime.utcnow)
    preliminary_at = Column(DateTime)
    finalized_at = Column(DateTime)
    amended_at = Column(DateTime)
    
    # 서명 정보
    dictated_by = Column(String(100))
    transcribed_by = Column(String(100))
    verified_by = Column(String(100))
    signed_by = Column(String(100))
    electronic_signature = Column(Text)
    
    # 배포 정보
    distributed_to = Column(Text)  # JSON 배열
    notification_sent = Column(Boolean, default=False)
    
    # 관계 설정
    patient = relationship("Patient", back_populates="diagnostic_reports")
    physician = relationship("Physician", back_populates="diagnostic_reports")
    
    def __repr__(self):
        return f"<DiagnosticReport(id={self.id}, patient={self.patient_id}, status={self.report_status})>"