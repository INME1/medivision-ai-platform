# MediVision AI Platform - Development Makefile

.PHONY: help setup dev dev-build stop restart logs shell test lint format clean db-migrate db-upgrade

# Default target
help:
	@echo "🏥 MediVision AI Platform - 개발 명령어"
	@echo ""
	@echo "설정 명령어:"
	@echo "  setup          - 개발환경 초기 설정"
	@echo "  dev            - 개발 서버 시작"
	@echo "  dev-build      - 이미지 재빌드 후 개발 서버 시작"
	@echo ""
	@echo "서비스 관리:"
	@echo "  stop           - 모든 서비스 중지"
	@echo "  restart        - 모든 서비스 재시작"
	@echo "  logs           - API 서버 로그 실시간 확인"
	@echo "  logs-all       - 모든 서비스 로그 확인"
	@echo ""
	@echo "개발 도구:"
	@echo "  shell          - API 컨테이너 셸 접속"
	@echo "  db-shell       - PostgreSQL 데이터베이스 접속"
	@echo "  redis-cli      - Redis CLI 접속"
	@echo ""
	@echo "코드 품질:"
	@echo "  test           - 테스트 실행"
	@echo "  test-cov       - 커버리지 포함 테스트 실행"
	@echo "  lint           - 코드 린팅 검사"
	@echo "  format         - 코드 자동 포맷팅"
	@echo ""
	@echo "데이터베이스:"
	@echo "  db-migrate     - 새로운 마이그레이션 생성"
	@echo "  db-upgrade     - 데이터베이스 스키마 업그레이드"
	@echo "  db-downgrade   - 데이터베이스 스키마 다운그레이드"
	@echo ""
	@echo "정리 작업:"
	@echo "  clean          - 컨테이너 및 볼륨 삭제"
	@echo "  clean-all      - 모든 Docker 리소스 정리"

# 개발환경 초기 설정
setup:
	@echo "🚀 개발환경 초기 설정 시작..."
	chmod +x scripts/dev-setup.sh
	./scripts/dev-setup.sh

# 개발 서버 시작
dev:
	@echo "🏥 MediVision AI Platform 개발 서버 시작..."
	docker-compose up

# 이미지 재빌드 후 개발 서버 시작
dev-build:
	@echo "🔨 이미지 재빌드 후 개발 서버 시작..."
	docker-compose up --build

# 백그라운드에서 개발 서버 시작
dev-daemon:
	@echo "🌙 백그라운드에서 개발 서버 시작..."
	docker-compose up -d

# 모든 서비스 중지
stop:
	@echo "⏹️ 모든 서비스 중지..."
	docker-compose down

# 모든 서비스 재시작
restart:
	@echo "🔄 모든 서비스 재시작..."
	docker-compose restart

# API 서버 로그 실시간 확인
logs:
	docker-compose logs -f api

# 모든 서비스 로그 확인
logs-all:
	docker-compose logs -f

# API 컨테이너 셸 접속
shell:
	docker-compose exec api bash

# PostgreSQL 데이터베이스 접속
db-shell:
	docker-compose exec postgres psql -U mediadmin -d medivision

# Redis CLI 접속
redis-cli:
	docker-compose exec redis redis-cli

# 테스트 실행
test:
	@echo "🧪 테스트 실행 중..."
	docker-compose exec api pytest -v

# 커버리지 포함 테스트 실행
test-cov:
	@echo "📊 커버리지 포함 테스트 실행 중..."
	docker-compose exec api pytest --cov=app --cov-report=html --cov-report=term-missing

# 코드 린팅 검사
lint:
	@echo "🔍 코드 린팅 검사 중..."
	docker-compose exec api flake8 app/
	docker-compose exec api mypy app/

# 코드 자동 포맷팅
format:
	@echo "✨ 코드 자동 포맷팅 중..."
	docker-compose exec api black app/
	docker-compose exec api isort app/

# 새로운 마이그레이션 생성
db-migrate:
	@read -p "마이그레이션 메시지를 입력하세요: " message; \
	docker-compose exec api alembic revision --autogenerate -m "$$message"

# 데이터베이스 스키마 업그레이드
db-upgrade:
	@echo "📈 데이터베이스 스키마 업그레이드 중..."
	docker-compose exec api alembic upgrade head

# 데이터베이스 스키마 다운그레이드
db-downgrade:
	@read -p "다운그레이드할 리비전을 입력하세요 (예: -1): " revision; \
	docker-compose exec api alembic downgrade $$revision

# 컨테이너 및 볼륨 삭제
clean:
	@echo "🧹 컨테이너 및 볼륨 정리 중..."
	docker-compose down -v
	docker-compose rm -f

# 모든 Docker 리소스 정리 (주의!)
clean-all:
	@echo "⚠️ 모든 Docker 리소스를 정리합니다!"
	@read -p "계속하시겠습니까? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		docker-compose down -v; \
		docker system prune -af; \
		docker volume prune -f; \
		echo "✅ Docker 리소스 정리 완료"; \
	else \
		echo "❌ 작업이 취소되었습니다"; \
	fi

# 서비스 상태 확인
status:
	@echo "📊 서비스 상태 확인..."
	docker-compose ps
	@echo ""
	@echo "🔗 서비스 URL:"
	@echo "  • API 서버: http://localhost:8000"
	@echo "  • API 문서: http://localhost:8000/docs"
	@echo "  • 데이터베이스 관리: http://localhost:8080"
	@echo "  • MinIO 콘솔: http://localhost:9001"
	@echo "  • Celery 모니터링: http://localhost:5555"

# 백업 생성
backup:
	@echo "💾 데이터베이스 백업 생성 중..."
	@mkdir -p backups
	@backup_file="backups/medivision_$(shell date +%Y%m%d_%H%M%S).sql"; \
	docker-compose exec postgres pg_dump -U mediadmin medivision > $$backup_file; \
	echo "✅ 백업 완료: $$backup_file"
