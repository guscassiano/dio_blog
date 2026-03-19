from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    nickname: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    nickname: str | None = None


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    nickname: str
    created_at: datetime | None = None
    active: bool
