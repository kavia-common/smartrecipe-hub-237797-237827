from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Display name")
    email: EmailStr = Field(..., description="Unique email address")
    password: str = Field(..., min_length=6, max_length=128, description="Account password")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Account email")
    password: str = Field(..., description="Account password")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type (always bearer)")
