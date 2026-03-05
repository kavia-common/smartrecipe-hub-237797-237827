from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from src.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return _pwd_context.hash(password)


# PUBLIC_INTERFACE
def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against its hash."""
    return _pwd_context.verify(password, password_hash)


# PUBLIC_INTERFACE
def create_access_token(subject: dict[str, Any], expires_minutes: int | None = None) -> str:
    """Create a signed JWT access token."""
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = dict(subject)
    payload.update({"exp": expire, "iat": datetime.now(tz=timezone.utc)})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


# PUBLIC_INTERFACE
def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
