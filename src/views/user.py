from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserReadMeView(BaseModel):
    id: int
    name: str
    email: EmailStr
    nickname: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserReadView(BaseModel):
    id: int
    name: str
    nickname: str

    model_config = ConfigDict(from_attributes=True)
