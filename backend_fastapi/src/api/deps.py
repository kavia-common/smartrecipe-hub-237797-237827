from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.security import decode_access_token
from src.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """Resolve the currently authenticated user from the Bearer token."""
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc

    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


# PUBLIC_INTERFACE
def require_admin(user: User = Depends(get_current_user)) -> User:
    """Dependency that ensures the current user is an admin."""
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
