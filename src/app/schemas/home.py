"""Schemas for aggregated home page bootstrap data."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.event import EventDetailRead, EventRead
from app.schemas.federation import FederationRead
from app.schemas.news import NewsRead
from app.schemas.result import ResultSummary
from app.schemas.roster import RosterRead
from app.schemas.user import UserRead


class HomeSnapshot(BaseModel):
    """Bundle of data required to render the landing page."""

    athletes: list[UserRead] = Field(default_factory=list)
    events: list[EventRead] = Field(default_factory=list)
    federations: list[FederationRead] = Field(default_factory=list)
    rosters: list[RosterRead] = Field(default_factory=list)
    results: list[ResultSummary] = Field(default_factory=list)
    news: list[NewsRead] = Field(default_factory=list)
    live_event: EventDetailRead | None = None
