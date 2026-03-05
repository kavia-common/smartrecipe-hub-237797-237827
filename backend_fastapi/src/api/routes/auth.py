from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.core.db import get_db
from src.core.security import create_access_token, hash_password, verify_password
from src.models import User
from src.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from src.schemas.user import UserPublic

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new account. Default role is `user`.",
    operation_id="auth_register",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserPublic:
    """Register a new user account."""
    existing = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")

    user = User(
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Authenticate using email + password and receive a JWT access token.",
    operation_id="auth_login",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate a user and return a JWT token."""
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Get current user",
    description="Returns the current authenticated user's profile.",
    operation_id="auth_me",
)
def me(user: User = Depends(get_current_user)) -> UserPublic:
    """Get the current authenticated user."""
    return user
