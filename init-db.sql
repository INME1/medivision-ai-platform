-- MediVision AI Platform Database Schema

-- 환자 정보
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),
    birth_date DATE,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 의료 영상
CREATE TABLE medical_images (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    study_id VARCHAR(100),
    series_id VARCHAR(100),
    image_id VARCHAR(100) UNIQUE NOT NULL,
    file_path VARCHAR(500),
    file_size INTEGER,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status VARCHAR(20) DEFAULT 'uploaded'
);

-- 영상 메타데이터
CREATE TABLE image_metadata (
    id SERIAL PRIMARY KEY,
    image_id VARCHAR(100) REFERENCES medical_images(image_id),
    modality VARCHAR(10),
    body_part VARCHAR(50),
    view_position VARCHAR(20),
    pixel_spacing_x FLOAT,
    pixel_spacing_y FLOAT,
    slice_thickness FLOAT,
    image_width INTEGER,
    image_height INTEGER,
    acquisition_date DATE,
    acquisition_time TIME,
    institution_name VARCHAR(200),
    manufacturer VARCHAR(100),
    model_name VARCHAR(100)
);

-- AI 예측 결과
CREATE TABLE ai_predictions (
    id SERIAL PRIMARY KEY,
    image_id VARCHAR(100) REFERENCES medical_images(image_id),
    model_name VARCHAR(100),
    model_version VARCHAR(20),
    prediction_class VARCHAR(100),
    confidence_score FLOAT,
    processing_time FLOAT,
    prediction_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 바운딩 박스 (객체 탐지 결과)
CREATE TABLE bounding_boxes (
    id SERIAL PRIMARY KEY,
    prediction_id INTEGER REFERENCES ai_predictions(id),
    x FLOAT,
    y FLOAT,
    width FLOAT,
    height FLOAT,
    label VARCHAR(100),
    confidence FLOAT
);

-- 의료진 정보
CREATE TABLE physicians (
    id SERIAL PRIMARY KEY,
    physician_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),
    specialty VARCHAR(100),
    license_number VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 의료진 검토
CREATE TABLE physician_reviews (
    id SERIAL PRIMARY KEY,
    prediction_id INTEGER REFERENCES ai_predictions(id),
    physician_id VARCHAR(50) REFERENCES physicians(physician_id),
    is_correct BOOLEAN,
    corrected_diagnosis VARCHAR(200),
    feedback TEXT,
    review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 진단 보고서
CREATE TABLE diagnostic_reports (
    id SERIAL PRIMARY KEY,
    image_id VARCHAR(100) REFERENCES medical_images(image_id),
    physician_id VARCHAR(50) REFERENCES physicians(physician_id),
    findings TEXT,
    impression TEXT,
    recommendations TEXT,
    report_status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finalized_at TIMESTAMP
);

-- 감사 로그
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50),
    action VARCHAR(100),
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 시스템 설정
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX idx_medical_images_patient_id ON medical_images(patient_id);
CREATE INDEX idx_medical_images_study_id ON medical_images(study_id);
CREATE INDEX idx_ai_predictions_image_id ON ai_predictions(image_id);
CREATE INDEX idx_ai_predictions_created_at ON ai_predictions(created_at);
CREATE INDEX idx_physician_reviews_prediction_id ON physician_reviews(prediction_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);

-- 기본 데이터 삽입
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('max_file_size', '100MB', '최대 업로드 파일 크기'),
('supported_formats', 'DICOM,JPEG,PNG', '지원되는 파일 형식'),
('ai_confidence_threshold', '0.8', 'AI 예측 신뢰도 임계값'),
('auto_review_enabled', 'true', '자동 검토 활성화 여부');

-- 샘플 의료진 데이터
INSERT INTO physicians (physician_id, name, specialty, license_number, email) VALUES
('DR001', 'Dr. Kim', 'Radiology', 'RAD2024001', 'dr.kim@hospital.com'),
('DR002', 'Dr. Lee', 'Emergency Medicine', 'EM2024001', 'dr.lee@hospital.com'),
('DR003', 'Dr. Park', 'Internal Medicine', 'IM2024001', 'dr.park@hospital.com');
