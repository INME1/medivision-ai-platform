from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.physician import Physician
from app.schemas.auth import Token, UserInfo
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 기본 관리자 계정 (하드코딩)
    if form_data.username == "admin" and form_data.password == "admin123":
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": "admin"}, 
            expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

@router.get("/me", response_model=UserInfo)
async def get_current_user():
    return UserInfo(
        physician_id="ADMIN001",
        name="시스템 관리자",
        username="admin",
        specialty="Administration"
    )
