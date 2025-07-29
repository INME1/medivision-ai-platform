#!/bin/bash

# MediVision AI Platform 개발환경 자동 설정 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                 MediVision AI Platform                       ║"
echo "║              개발환경 자동 설정 스크립트                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 함수 정의
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 필수 도구 확인
check_requirements() {
    log_info "필수 도구 확인 중..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker가 설치되지 않았습니다. Docker를 먼저 설치해주세요."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose가 설치되지 않았습니다."
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        log_error "Git이 설치되지 않았습니다."
        exit 1
    fi
    
    log_success "필수 도구 확인 완료"
}

# Python 가상환경 설정 (로컬 개발용)
setup_python_env() {
    log_info "Python 가상환경 설정 중..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_success "Python 가상환경이 생성되었습니다."
    fi
    
    # 가상환경 활성화 및 패키지 설치
    source venv/bin/activate
    pip install --upgrade pip
    
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
        log_success "Python 패키지 설치 완료"
    else
        log_warning "requirements.txt 파일이 없습니다."
    fi
}

# Docker 서비스 시작
start_docker_services() {
    log_info "Docker 서비스 시작 중..."
    
    # 기존 컨테이너 정리
    docker-compose down -v 2>/dev/null || true
    
    # 새로운 컨테이너 빌드 및 시작
    docker-compose up -d --build
    
    log_info "서비스 준비 대기 중..."
    sleep 10
    
    # 서비스 상태 확인
    if docker-compose ps | grep -q "Up"; then
        log_success "Docker 서비스가 성공적으로 시작되었습니다."
    else
        log_error "Docker 서비스 시작에 실패했습니다."
        exit 1
    fi
}

# 데이터베이스 초기화
init_database() {
    log_info "데이터베이스 초기화 중..."
    
    # 데이터베이스 연결 대기
    for i in {1..30}; do
        if docker-compose exec -T postgres pg_isready -U mediadmin -d medivision &>/dev/null; then
            break
        fi
        sleep 1
    done
    
    log_success "데이터베이스 초기화 완료"
}

# MinIO 버킷 생성
setup_minio() {
    log_info "MinIO 스토리지 설정 중..."
    
    # MinIO 클라이언트 설치 및 설정
    docker-compose exec -T minio bash -c "
        mc alias set myminio http://localhost:9000 minioadmin minioadmin123
        mc mb myminio/medivision-storage --ignore-existing
        mc mb myminio/dicom-files --ignore-existing
        mc mb myminio/processed-images --ignore-existing
    " 2>/dev/null || log_warning "MinIO 버킷 생성을 건너뜁니다."
    
    log_success "MinIO 스토리지 설정 완료"
}

# 서비스 URL 정보 출력
show_service_info() {
    echo -e "\n${GREEN}🎉 개발환경 설정이 완료되었습니다!${NC}\n"
    
    echo -e "${BLUE}📍 서비스 접속 정보:${NC}"
    echo "   • API 서버: http://localhost:8000"
    echo "   • API 문서: http://localhost:8000/docs"
    echo "   • 데이터베이스 관리: http://localhost:8080"
    echo "   • MinIO 콘솔: http://localhost:9001 (minioadmin/minioadmin123)"
    echo "   • Celery 모니터링: http://localhost:5555"
    echo "   • Redis: localhost:6379"
    echo "   • PostgreSQL: localhost:5432"
    
    echo -e "\n${BLUE}🛠️ 유용한 명령어:${NC}"
    echo "   • make dev          # 개발 서버 시작"
    echo "   • make logs         # API 서버 로그 확인"
    echo "   • make shell        # API 컨테이너 접속"
    echo "   • make test         # 테스트 실행"
    echo "   • make clean        # 모든 컨테이너 및 볼륨 삭제"
    
    echo -e "\n${YELLOW}⚠️ 다음 단계:${NC}"
    echo "   1. .env 파일의 설정을 확인하고 필요시 수정하세요"
    echo "   2. backend/main.py 파일을 생성하여 FastAPI 애플리케이션을 구현하세요"
    echo "   3. Colab에서 훈련된 모델을 models/ 디렉토리에 복사하세요"
    echo "   4. 'make dev' 명령어로 개발을 시작하세요"
}

# 메인 실행 함수
main() {
    check_requirements
    setup_python_env
    start_docker_services
    init_database
    setup_minio
    show_service_info
}

# 스크립트 실행
main "$@"
