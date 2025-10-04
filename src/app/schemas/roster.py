from datetime import datetime

from pydantic import BaseModel, Field


class RosterBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    country: str = Field(..., min_length=2, max_length=80)
    division: str = Field(..., min_length=1, max_length=80)
    coach_name: str = Field(..., min_length=3, max_length=120)
    athlete_count: int = Field(default=0, ge=0)


class RosterCreate(RosterBase):
    pass


class RosterRead(RosterBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
