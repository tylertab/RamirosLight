from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.user import EmailField


class EmailSubscriberCreate(BaseModel):
    email: EmailField
    locale: str | None = Field(default=None, min_length=2, max_length=10)


class EmailSubscriberRead(BaseModel):
    id: int
    email: EmailField
    locale: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
