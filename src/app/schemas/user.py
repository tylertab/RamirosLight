from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


BASIC_EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

EmailField = Annotated[
    str,
    Field(
        ...,
        min_length=3,
        max_length=320,
        pattern=BASIC_EMAIL_PATTERN,
        description="Basic email validation pattern (avoids external email-validator dependency)",
    ),
]


class UserBase(BaseModel):
    email: EmailField
    full_name: str = Field(..., min_length=1, max_length=120)
    role: str = Field(..., description="Role within the ecosystem: fan, athlete, coach, federation, scout")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
