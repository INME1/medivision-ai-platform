from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

from app.core.config import settings

# 로거 설정
logger = logging.getLogger(__name__)

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.database_url_sync,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=3600,   # 1시간마다 연결 재생성
    echo=settings.DEBUG,  # 개발 환경에서 SQL 쿼리 로깅
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base 클래스 생성 (모든 모델의 부모 클래스)
Base = declarative_base()

# 메타데이터 설정
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션 의존성 주입용 함수
    FastAPI의 Depends에서 사용
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """
    모든 테이블 생성
    애플리케이션 시작 시 호출
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


def drop_tables():
    """
    모든 테이블 삭제
    테스트나 초기화 시 사용
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop database tables: {e}")
        raise


def check_db_connection() -> bool:
    """
    데이터베이스 연결 상태 확인
    헬스체크에서 사용
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Database connection is healthy")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def get_session(self) -> Session:
        """새로운 데이터베이스 세션 반환"""
        return self.SessionLocal()
    
    def execute_query(self, query: str, params: dict = None):
        """직접 SQL 쿼리 실행"""
        with self.engine.connect() as connection:
            if params:
                result = connection.execute(query, params)
            else:
                result = connection.execute(query)
            return result.fetchall()
    
    def get_table_info(self, table_name: str):
        """테이블 정보 조회"""
        query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = :table_name
        ORDER BY ordinal_position;
        """
        return self.execute_query(query, {"table_name": table_name})
    
    def backup_table(self, table_name: str, backup_name: str = None):
        """테이블 백업"""
        if not backup_name:
            from datetime import datetime
            backup_name = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        query = f"CREATE TABLE {backup_name} AS SELECT * FROM {table_name};"
        self.execute_query(query)
        logger.info(f"Table {table_name} backed up as {backup_name}")


# 전역 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager()


# 데이터베이스 초기화 함수
def init_db():
    """
    데이터베이스 초기화
    애플리케이션 시작 시 호출
    """
    try:
        # 연결 테스트
        if not check_db_connection():
            raise Exception("Database connection failed")
        
        # 테이블 생성
        create_tables()
        
        # 초기 데이터 확인
        from app.core.init_data import init_sample_data
        init_sample_data()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


# 테스트용 데이터베이스 설정
def get_test_db():
    """테스트용 데이터베이스 세션"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # 테스트용 인메모리 SQLite 사용
    test_engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=test_engine
    )
    
    # 테스트용 테이블 생성
    Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()