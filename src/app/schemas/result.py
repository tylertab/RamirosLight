"""Schemas describing competition result summaries."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ResultSummary(BaseModel):
    """Lightweight projection of an event entry with context."""

    entry_id: int = Field(..., description="Primary identifier for the entry")
    event_id: int = Field(..., description="Identifier of the parent event")
    event_name: str = Field(..., description="Name of the parent event")
    event_location: str | None = Field(default=None, description="City or venue of the event")
    discipline_id: int = Field(..., description="Identifier of the discipline")
    discipline_name: str = Field(..., description="Discipline where the entry competed")
    discipline_round: str | None = Field(
        default=None, description="Round or heat of the discipline when available"
    )
    athlete_name: str = Field(..., description="Name of the athlete or relay")
    team_name: str | None = Field(default=None, description="Club or roster associated with the entry")
    position: int | None = Field(default=None, description="Final placing or rank for the entry")
    result: str | None = Field(default=None, description="Performance mark, e.g. 10.12s or 6.45m")
    updated_at: datetime = Field(..., description="Timestamp of the most recent update")
