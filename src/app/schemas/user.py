from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.domain import SubscriptionTier


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
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE


class UserRead(UserBase):
    id: int
    created_at: datetime
    subscription_expires_at: datetime | None = None
    subscription_started_at: datetime | None = None

    class Config:
        from_attributes = True
