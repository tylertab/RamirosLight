from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AthleteSummary(BaseModel):
    id: int
    full_name: str
    email: str
    bio: str | None = None


class AthleteRosterSummary(BaseModel):
    id: int
    name: str
    country: str
    division: str
    coach_name: str
    athlete_count: int
    updated_at: datetime

    class Config:
        from_attributes = True


class AthleteHistoryEntry(BaseModel):
    event: str
    event_date: str
    result: str
    video_url: str | None = None


class AthleteProfileRead(BaseModel):
    user_id: int
    bio: str | None = None
    track_history: list[AthleteHistoryEntry] = Field(default_factory=list)
    highlight_video_url: str | None = None


class AthleteProfileUpdate(BaseModel):
    bio: str | None = Field(default=None, max_length=500)
    track_history: list[AthleteHistoryEntry] | None = None
    highlight_video_url: str | None = Field(default=None, max_length=500)


class AthleteHistoryResponse(BaseModel):
    athlete_id: int
    history: list[AthleteHistoryEntry]

    class Config:
        arbitrary_types_allowed = True


class AthleteDetail(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    subscription_tier: str
    created_at: datetime
    updated_at: datetime
    bio: str | None = None
    track_history: list[AthleteHistoryEntry] = Field(default_factory=list)
    highlight_video_url: str | None = None
    rosters: list[AthleteRosterSummary] = Field(default_factory=list)
