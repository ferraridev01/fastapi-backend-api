from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user_model import User
from app.schemas.user_schema import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = (
        db.query(User)
        .filter((User.username == user_data.username) | (User.email == user_data.email))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(
    db: Session, login_data: OAuth2PasswordRequestForm
) -> User | None:
    db_user = db.query(User).filter(User.username == login_data.username).first()
    if not db_user:
        return None

    if not verify_password(login_data.password, db_user.hashed_password):
        return None

    return db_user


def login_user(db: Session, login_data: OAuth2PasswordRequestForm) -> dict[str, str]:
    db_user = authenticate_user(db, login_data)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": db_user.username}
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}
