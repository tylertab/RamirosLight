"""Schemas for aggregated home page bootstrap data."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.event import EventDetailRead, EventRead
from app.schemas.news import NewsRead


class HomeRoster(BaseModel):
    """Lightweight roster summary nested under a club."""

    id: int | None = None
    name: str
    division: str | None = None
    coach_name: str | None = None
    athlete_count: int | None = None
    updated_at: datetime | None = None


class HomeClub(BaseModel):
    """Representation of a club surfaced on the home page."""

    id: int
    name: str
    city: str | None = None
    country: str | None = None
    rosters: list[HomeRoster] = Field(default_factory=list)


class HomeFederation(BaseModel):
    """Federation and the clubs highlighted for the landing page."""

    id: int
    name: str
    country: str | None = None
    website: str | None = None
    clubs: list[HomeClub] = Field(default_factory=list)


class HomeResult(BaseModel):
    """Recent event entry surfaced on the landing page."""

    entry_id: int
    event_id: int
    event_name: str
    discipline_id: int
    discipline_name: str
    athlete_name: str
    team_name: str | None = None
    position: int | None = None
    result: str | None = None
    points: int | None = None
    roster_id: int | None = None
    roster_name: str | None = None
    club_id: int | None = None
    club_name: str | None = None
    federation_id: int | None = None
    federation_name: str | None = None
    updated_at: datetime | None = None


class HomeSnapshot(BaseModel):
    """Bundle of data required to render the landing page."""

    federations: list[HomeFederation] = Field(default_factory=list)
    events: list[EventRead] = Field(default_factory=list)
    recent_results: list[HomeResult] = Field(default_factory=list)
    news: list[NewsRead] = Field(default_factory=list)
    live_event: EventDetailRead | None = None
