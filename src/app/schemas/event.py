from datetime import date, datetime
from enum import Enum

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


class EventSessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"


class EventDisciplineStatus(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    DELAYED = "delayed"
    FINALIZED = "finalized"


class EventEntryStatus(str, Enum):
    SCHEDULED = "scheduled"
    READY = "ready"
    LIVE = "live"
    FINISHED = "finished"
    DNS = "dns"
    DQ = "dq"


class EventSessionBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=120)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    venue: str | None = Field(default=None, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    status: EventSessionStatus = Field(default=EventSessionStatus.SCHEDULED)


class EventSessionCreate(EventSessionBase):
    pass


class EventSessionRead(EventSessionBase):
    id: int

    class Config:
        from_attributes = True


class EventDisciplineBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=120)
    category: str | None = Field(default=None, max_length=60)
    round_name: str | None = Field(default=None, max_length=80)
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    status: EventDisciplineStatus = Field(default=EventDisciplineStatus.SCHEDULED)
    venue: str | None = Field(default=None, max_length=120)
    order: int | None = None


class EventDisciplineCreate(EventDisciplineBase):
    session_id: int | None = Field(default=None)


class EventRosterStub(BaseModel):
    id: int
    name: str
    country: str | None = None

    class Config:
        from_attributes = True


class EventEntryBase(BaseModel):
    athlete_name: str = Field(..., min_length=1, max_length=120)
    team_name: str | None = Field(default=None, max_length=120)
    bib: str | None = Field(default=None, max_length=20)
    lane: str | None = Field(default=None, max_length=12)
    seed_mark: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=500)
    status: EventEntryStatus = Field(default=EventEntryStatus.SCHEDULED)


class EventEntryCreate(EventEntryBase):
    roster_id: int | None = Field(default=None)


class EventEntryUpdate(BaseModel):
    athlete_name: str | None = Field(default=None, min_length=1, max_length=120)
    team_name: str | None = Field(default=None, max_length=120)
    bib: str | None = Field(default=None, max_length=20)
    lane: str | None = Field(default=None, max_length=12)
    seed_mark: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=500)
    status: EventEntryStatus | None = None
    position: int | None = Field(default=None, ge=1)
    result: str | None = Field(default=None, max_length=60)
    points: int | None = None


class EventEntryRead(EventEntryBase):
    id: int
    position: int | None = None
    result: str | None = None
    points: int | None = None
    roster_id: int | None = None
    roster: EventRosterStub | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class EventDisciplineRead(EventDisciplineBase):
    id: int
    session_id: int | None = None
    session: EventSessionRead | None = None
    entries: list[EventEntryRead] = Field(default_factory=list)

    class Config:
        from_attributes = True


class EventDetailRead(EventRead):
    sessions: list[EventSessionRead] = Field(default_factory=list)
    disciplines: list[EventDisciplineRead] = Field(default_factory=list)
    latest_update: datetime | None = None


class EventFakeTimelineRequest(BaseModel):
    start_time: datetime | None = Field(default=None, description="Anchor time for first session")
    sessions: int = Field(default=2, ge=1, le=6)
    disciplines_per_session: int = Field(default=3, ge=1, le=10)
    lanes: int = Field(default=8, ge=2, le=12)
    include_results: bool = Field(default=True)
