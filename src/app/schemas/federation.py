from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.federation import FederationSubmissionStatus
from app.schemas.user import EmailField, UserRead


class FederationBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=120)
    country: str | None = Field(default=None, max_length=80)
    website: str | None = Field(default=None, max_length=255)


class FederationSummary(FederationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FederationRosterSummary(BaseModel):
    id: int
    name: str
    division: str
    coach_name: str
    athlete_count: int

    model_config = ConfigDict(from_attributes=True)


class ClubBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    city: str | None = Field(default=None, max_length=120)
    country: str = Field(..., min_length=2, max_length=80)


class ClubCreate(ClubBase):
    federation_id: int | None = Field(default=None, ge=1)


class ClubSummary(ClubBase):
    id: int
    federation_id: int | None = None
    manager: UserRead | None = None

    model_config = ConfigDict(from_attributes=True)


class ClubWithRosters(ClubSummary):
    rosters: list[FederationRosterSummary] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class FederationWithClubs(FederationSummary):
    clubs: list[ClubWithRosters] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class FederationSubmissionBase(BaseModel):
    federation_name: str = Field(..., min_length=3, max_length=120)
    contact_email: EmailField
    payload_url: str = Field(..., description="Public or signed URL where the result file can be fetched")
    notes: str | None = Field(default=None, max_length=500)


class FederationSubmissionCreate(FederationSubmissionBase):
    pass


class FederationSubmissionRead(FederationSubmissionBase):
    id: int
    status: FederationSubmissionStatus
    submitted_at: datetime = Field(alias="created_at")
    processed_at: datetime | None = None
    verified_at: datetime | None = None
    status_details: str | None = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
