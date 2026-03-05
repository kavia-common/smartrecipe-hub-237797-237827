from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserPublic(BaseModel):
    id: int = Field(..., description="User id")
    name: str = Field(..., description="Display name")
    email: EmailStr = Field(..., description="Email address")
    role: str = Field(..., description="Role: user|admin")
    created_at: datetime = Field(..., description="Created timestamp")

    class Config:
        from_attributes = True
