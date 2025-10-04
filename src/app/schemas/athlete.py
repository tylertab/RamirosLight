from typing import Any

from pydantic import BaseModel, Field


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
