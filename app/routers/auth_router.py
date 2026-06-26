from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user_schema import (
    AccessTokenResponse,
    RefreshTokenRequest,
    Token,
    UserCreate,
    UserResponse,
)
from app.services.auth_service import create_user, login_user, refresh_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return login_user(db, login_data)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_access_token_route(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(db, token_data.refresh_token)
