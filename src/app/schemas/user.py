from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=120)
    role: str = Field(..., description="Role within the ecosystem: fan, athlete, coach, federation, scout")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
