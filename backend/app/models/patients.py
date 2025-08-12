from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date

from app.core.database import Base


class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100))
    birth_date = Column(Date)
    gender = Column(String(10))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    emergency_contact = Column(String(100))
    medical_history = Column(Text)
    allergies = Column(Text)
    current_medications = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    medical_images = relationship("MedicalImage", back_populates="patient")
    diagnostic_reports = relationship("DiagnosticReport", back_populates="patient")
    
    def __repr__(self):
        return f"<Patient(id={self.patient_id}, name={self.name})>"
    
    @property
    def age(self) -> int:
        """나이 계산"""
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return 0


# backend/app/models/image.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class MedicalImage(Base):
    __tablename__ = "medical_images"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), ForeignKey("patients.patient_id"), nullable=False)
    study_id = Column(String(100), index=True)
    series_id = Column(String(100))
    image_id = Column(String(100), unique=True, nullable=False, index=True)
    
    # 파일 정보
    file_path = Column(String(500))
    file_name = Column(String(255))
    file_size = Column(Integer)
    file_hash = Column(String(64))  # SHA-256 해시
    original_filename = Column(String(255))
    mime_type = Column(String(100))
    
    # 처리 상태
    processing_status = Column(String(20), default="uploaded")  # uploaded, processing, completed, failed
    upload_time = Column(DateTime, default=datetime.utcnow)
    processing_started_at = Column(DateTime)
    processing_completed_at = Column(DateTime)
    
    # 관계 설정
    patient = relationship("Patient", back_populates="medical_images")
    metadata = relationship("ImageMetadata", back_populates="medical_image", uselist=False)
    predictions = relationship("AIPrediction", back_populates="medical_image")
    
    def __repr__(self):
        return f"<MedicalImage(id={self.image_id}, patient={self.patient_id})>"


class ImageMetadata(Base):
    __tablename__ = "image_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(String(100), ForeignKey("medical_images.image_id"), nullable=False)
    
    # DICOM 메타데이터
    modality = Column(String(10))  # CT, MRI, X-ray, US 등
    body_part = Column(String(50))
    view_position = Column(String(20))
    study_description = Column(String(200))
    series_description = Column(String(200))
    
    # 이미지 속성
    pixel_spacing_x = Column(Float)
    pixel_spacing_y = Column(Float)
    slice_thickness = Column(Float)
    image_width = Column(Integer)
    image_height = Column(Integer)
    bits_allocated = Column(Integer)
    bits_stored = Column(Integer)
    
    # 장비 정보
    manufacturer = Column(String(100))
    model_name = Column(String(100))
    software_version = Column(String(50))
    
    # 촬영 정보
    acquisition_date = Column(Date)
    acquisition_time = Column(DateTime)
    kvp = Column(Float)  # 촬영 전압
    exposure_time = Column(Float)
    institution_name = Column(String(200))
    referring_physician = Column(String(100))
    
    # 추가 메타데이터 (JSON)
    additional_metadata = Column(Text)  # JSON 형태로 저장
    
    # 관계 설정
    medical_image = relationship("MedicalImage", back_populates="metadata")
    
    def __repr__(self):
        return f"<ImageMetadata(image_id={self.image_id}, modality={self.modality})>"


# backend/app/models/prediction.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class AIPrediction(Base):
    __tablename__ = "ai_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(String(100), ForeignKey("medical_images.image_id"), nullable=False)
    
    # 모델 정보
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(20))
    model_type = Column(String(50))  # classification, detection, segmentation
    
    # 예측 결과
    prediction_class = Column(String(100))
    confidence_score = Column(Float)
    prediction_probability = Column(Float)
    
    # 처리 정보
    processing_time = Column(Float)  # 초 단위
    prediction_timestamp = Column(DateTime, default=datetime.utcnow)
    gpu_used = Column(Boolean, default=False)
    
    # 상세 결과 데이터
    prediction_data = Column(JSON)  # 전체 예측 결과 JSON
    feature_map_path = Column(String(500))  # Feature map 이미지 경로
    heatmap_path = Column(String(500))  # 히트맵 이미지 경로
    
    # 검증 상태
    is_reviewed = Column(Boolean, default=False)
    review_status = Column(String(20), default="pending")  # pending, approved, rejected
    
    # 관계 설정
    medical_image = relationship("MedicalImage", back_populates="predictions")
    bounding_boxes = relationship("BoundingBox", back_populates="prediction")
    physician_reviews = relationship("PhysicianReview", back_populates="prediction")
    
    def __repr__(self):
        return f"<AIPrediction(id={self.id}, class={self.prediction_class}, confidence={self.confidence_score})>"


class BoundingBox(Base):
    __tablename__ = "bounding_boxes"
    
    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("ai_predictions.id"), nullable=False)
    
    # 바운딩 박스 좌표 (normalized 0-1)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    
    # 라벨 정보
    label = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    class_id = Column(Integer)
    
    # 추가 정보
    area = Column(Float)
    is_abnormal = Column(Boolean, default=False)
    severity_score = Column(Float)  # 0-1, 심각도
    
    # 관계 설정
    prediction = relationship("AIPrediction", back_populates="bounding_boxes")
    
    def __repr__(self):
        return f"<BoundingBox(label={self.label}, confidence={self.confidence})>"
