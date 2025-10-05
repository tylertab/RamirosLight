from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.athlete import AthleteSummary
from app.schemas.federation import ClubCreate, ClubSummary, FederationSummary
from app.schemas.user import UserRead


class RosterBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    country: str = Field(..., min_length=2, max_length=80)
    division: str = Field(..., min_length=1, max_length=80)
    coach_name: str = Field(..., min_length=3, max_length=120)
    athlete_count: int = Field(default=0, ge=0)


class RosterCreate(RosterBase):
    club_id: int | None = Field(default=None, ge=1)
    club: ClubCreate | None = None

    @model_validator(mode="after")
    def validate_club(self) -> "RosterCreate":
        if self.club_id is None and self.club is None:
            raise ValueError("Club reference or details must be provided")
        return self


class RosterRead(RosterBase):
    id: int
    updated_at: datetime
    club: ClubSummary | None = None
    federation: FederationSummary | None = None

    model_config = ConfigDict(from_attributes=True)


class RosterDetail(RosterRead):
    owner: UserRead | None = None
    athletes: list[AthleteSummary] = Field(default_factory=list)
