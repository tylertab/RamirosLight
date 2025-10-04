from datetime import date

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=120)
    location: str = Field(..., min_length=2, max_length=120)
    start_date: date
    end_date: date
    federation_id: int | None = Field(default=None, description="Organizing federation ID")


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int

    class Config:
        from_attributes = True
