from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    federation_id: Mapped[int | None] = mapped_column(ForeignKey("federations.id"), nullable=True)
    sessions: Mapped[list["EventSession"]] = relationship(
        "EventSession",
        back_populates="event",
        cascade="all, delete-orphan",
        order_by="EventSession.start_time",
    )
    disciplines: Mapped[list["EventDiscipline"]] = relationship(
        "EventDiscipline",
        back_populates="event",
        cascade="all, delete-orphan",
        order_by="EventDiscipline.scheduled_start",
    )


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


class EventSession(Base):
    __tablename__ = "event_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    venue: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[EventSessionStatus] = mapped_column(
        SqlEnum(EventSessionStatus, name="event_session_status"),
        default=EventSessionStatus.SCHEDULED,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    event: Mapped[Event] = relationship("Event", back_populates="sessions")
    disciplines: Mapped[list["EventDiscipline"]] = relationship(
        "EventDiscipline",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="EventDiscipline.scheduled_start",
    )


class EventDiscipline(Base):
    __tablename__ = "event_disciplines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    session_id: Mapped[int | None] = mapped_column(
        ForeignKey("event_sessions.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str | None] = mapped_column(String(60), nullable=True)
    round_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[EventDisciplineStatus] = mapped_column(
        SqlEnum(EventDisciplineStatus, name="event_discipline_status"),
        default=EventDisciplineStatus.SCHEDULED,
        nullable=False,
    )
    venue: Mapped[str | None] = mapped_column(String(120), nullable=True)
    order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    event: Mapped[Event] = relationship("Event", back_populates="disciplines")
    session: Mapped[EventSession | None] = relationship("EventSession", back_populates="disciplines")
    entries: Mapped[list["EventEntry"]] = relationship(
        "EventEntry",
        back_populates="discipline",
        cascade="all, delete-orphan",
        order_by="EventEntry.lane",
    )


class EventEntry(Base):
    __tablename__ = "event_entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    discipline_id: Mapped[int] = mapped_column(
        ForeignKey("event_disciplines.id", ondelete="CASCADE"), nullable=False
    )
    roster_id: Mapped[int | None] = mapped_column(
        ForeignKey("rosters.id", ondelete="SET NULL"), nullable=True
    )
    athlete_name: Mapped[str] = mapped_column(String(120), nullable=False)
    team_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    bib: Mapped[str | None] = mapped_column(String(20), nullable=True)
    lane: Mapped[str | None] = mapped_column(String(12), nullable=True)
    seed_mark: Mapped[str | None] = mapped_column(String(40), nullable=True)
    status: Mapped[EventEntryStatus] = mapped_column(
        SqlEnum(EventEntryStatus, name="event_entry_status"),
        default=EventEntryStatus.SCHEDULED,
        nullable=False,
    )
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    result: Mapped[str | None] = mapped_column(String(60), nullable=True)
    points: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    discipline: Mapped[EventDiscipline] = relationship("EventDiscipline", back_populates="entries")
    roster: Mapped["Roster | None"] = relationship("Roster", lazy="joined")


__all__ = [
    "Event",
    "EventSession",
    "EventDiscipline",
    "EventEntry",
    "EventSessionStatus",
    "EventDisciplineStatus",
    "EventEntryStatus",
]
