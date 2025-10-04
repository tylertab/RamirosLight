from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import sample

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_session
from app.models import (
    Event,
    EventDiscipline,
    EventDisciplineStatus,
    EventEntry,
    EventEntryStatus,
    EventSession,
    EventSessionStatus,
)
from app.schemas.event import (
    EventCreate,
    EventDetailRead,
    EventDisciplineCreate,
    EventDisciplineRead,
    EventEntryCreate,
    EventEntryRead,
    EventEntryUpdate,
    EventFakeTimelineRequest,
    EventRead,
    EventSessionCreate,
    EventSessionRead,
)


class EventsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _require_event(self, event_id: int) -> Event:
        event = await self._session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    async def _require_session(self, session_id: int) -> EventSession:
        session = await self._session.get(EventSession, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Event session not found")
        return session

    async def _require_discipline(self, discipline_id: int) -> EventDiscipline:
        discipline = await self._session.get(EventDiscipline, discipline_id)
        if not discipline:
            raise HTTPException(status_code=404, detail="Event discipline not found")
        return discipline

    async def _require_entry(self, entry_id: int) -> EventEntry:
        entry = await self._session.get(EventEntry, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Event entry not found")
        return entry

    async def create_event(self, payload: EventCreate) -> EventRead:
        event = Event(**payload.model_dump())
        self._session.add(event)
        await self._session.commit()
        await self._session.refresh(event)
        return EventRead.model_validate(event)

    async def list_events(self) -> list[EventRead]:
        result = await self._session.execute(select(Event))
        events = result.scalars().all()
        return [EventRead.model_validate(event) for event in events]

    async def get_event_detail(self, event_id: int) -> EventDetailRead:
        result = await self._session.execute(
            select(Event)
                .where(Event.id == event_id)
                .options(
                    selectinload(Event.sessions),
                    selectinload(Event.disciplines)
                    .options(
                        selectinload(EventDiscipline.session),
                        selectinload(EventDiscipline.entries).selectinload(EventEntry.roster),
                    ),
                )
        )
        event = result.scalar_one_or_none()
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        detail = EventDetailRead.model_validate(event)

        latest_update: datetime | None = None
        for discipline in event.disciplines:
            for entry in discipline.entries:
                if entry.updated_at is not None and (
                    latest_update is None or entry.updated_at > latest_update
                ):
                    latest_update = entry.updated_at
        detail.latest_update = latest_update
        return detail

    async def create_session(
        self, event_id: int, payload: EventSessionCreate
    ) -> EventSessionRead:
        await self._require_event(event_id)
        session = EventSession(event_id=event_id, **payload.model_dump())
        self._session.add(session)
        await self._session.commit()
        await self._session.refresh(session)
        return EventSessionRead.model_validate(session)

    async def create_discipline(
        self, event_id: int, payload: EventDisciplineCreate
    ) -> EventDisciplineRead:
        await self._require_event(event_id)
        if payload.session_id is not None:
            session = await self._require_session(payload.session_id)
            if session.event_id != event_id:
                raise HTTPException(status_code=400, detail="Session does not belong to event")
        discipline = EventDiscipline(event_id=event_id, **payload.model_dump())
        self._session.add(discipline)
        await self._session.commit()
        await self._session.refresh(discipline, attribute_names=["entries", "session"])
        return EventDisciplineRead.model_validate(discipline)

    async def create_entry(
        self, discipline_id: int, payload: EventEntryCreate
    ) -> EventEntryRead:
        discipline = await self._require_discipline(discipline_id)
        entry = EventEntry(discipline_id=discipline.id, **payload.model_dump())
        self._session.add(entry)
        await self._session.commit()
        await self._session.refresh(entry, attribute_names=["roster", "updated_at"])
        return EventEntryRead.model_validate(entry)

    async def update_entry(self, entry_id: int, payload: EventEntryUpdate) -> EventEntryRead:
        entry = await self._require_entry(entry_id)
        data = payload.model_dump(exclude_unset=True)
        if not data:
            return EventEntryRead.model_validate(entry)
        for key, value in data.items():
            setattr(entry, key, value)
        self._session.add(entry)
        await self._session.commit()
        await self._session.refresh(entry, attribute_names=["roster", "updated_at"])
        return EventEntryRead.model_validate(entry)

    async def generate_fake_timeline(
        self, event_id: int, payload: EventFakeTimelineRequest
    ) -> EventDetailRead:
        await self._require_event(event_id)

        # Clear existing structure for a clean demo slate.
        await self._session.execute(
            delete(EventEntry).where(
                EventEntry.discipline_id.in_(
                    select(EventDiscipline.id).where(EventDiscipline.event_id == event_id)
                )
            )
        )
        await self._session.execute(
            delete(EventDiscipline).where(EventDiscipline.event_id == event_id)
        )
        await self._session.execute(delete(EventSession).where(EventSession.event_id == event_id))

        base_start = payload.start_time or datetime.now(tz=timezone.utc)
        session_templates = [
            "Opening Session",
            "Morning Heats",
            "Afternoon Finals",
            "Golden Night",
            "Relay Showcase",
            "Closing Ceremony",
        ]
        discipline_templates = [
            ("100m", "Sprints"),
            ("200m", "Sprints"),
            ("400m", "Sprints"),
            ("800m", "Middle Distance"),
            ("1500m", "Middle Distance"),
            ("5000m", "Distance"),
            ("110m Hurdles", "Hurdles"),
            ("400m Hurdles", "Hurdles"),
            ("Long Jump", "Jumps"),
            ("Triple Jump", "Jumps"),
            ("High Jump", "Jumps"),
            ("Pole Vault", "Jumps"),
            ("Shot Put", "Throws"),
            ("Discus Throw", "Throws"),
            ("Javelin Throw", "Throws"),
            ("4x100m Relay", "Relays"),
            ("4x400m Relay", "Relays"),
        ]
        team_names = [
            "Andean Flyers",
            "Caribbean Storm",
            "Patagonia Peaks",
            "Amazon Striders",
            "Pacífico Runners",
            "Altiplano Club",
            "Granada Hurdlers",
            "Cusco Distance",
            "Quito Relays",
            "Buenos Aires Elite",
            "Montevideo Vault",
            "Santiago Throws",
        ]
        athlete_names = [
            "Valentina Ríos",
            "Mateo Herrera",
            "Camila Ibáñez",
            "Thiago López",
            "Luisa Carvalho",
            "Daniel Torres",
            "Renata Gómez",
            "Pablo Medina",
            "Sofía Vargas",
            "Gabriel da Costa",
            "Mariana Núñez",
            "Felipe Cruz",
        ]

        sessions: list[EventSession] = []
        for index in range(payload.sessions):
            session = EventSession(
                event_id=event_id,
                name=session_templates[index % len(session_templates)],
                start_time=base_start + timedelta(hours=index * 3),
                end_time=base_start + timedelta(hours=(index * 3) + 2),
                venue="Main Stadium",
                status=EventSessionStatus.LIVE
                if index == 0
                else EventSessionStatus.SCHEDULED,
                description="Automatically generated for demo purposes.",
            )
            self._session.add(session)
            sessions.append(session)

        await self._session.flush()

        lane_range = list(range(1, payload.lanes + 1))
        generated_disciplines: list[EventDiscipline] = []

        for session_index, session in enumerate(sessions):
            for slot in range(payload.disciplines_per_session):
                template_index = (session_index * payload.disciplines_per_session + slot) % len(
                    discipline_templates
                )
                name, category = discipline_templates[template_index]
                scheduled_start = (session.start_time or base_start) + timedelta(minutes=slot * 45)
                scheduled_end = scheduled_start + timedelta(minutes=35)
                status = (
                    EventDisciplineStatus.FINALIZED
                    if payload.include_results and session_index == 0 and slot == 0
                    else EventDisciplineStatus.LIVE
                    if session_index == 0 and slot == 1
                    else EventDisciplineStatus.SCHEDULED
                )
                discipline = EventDiscipline(
                    event_id=event_id,
                    session_id=session.id,
                    name=name,
                    category=category,
                    round_name="Final" if slot % 2 == 0 else "Semi-final",
                    scheduled_start=scheduled_start,
                    scheduled_end=scheduled_end,
                    status=status,
                    venue="Main Stadium",
                    order=slot + 1,
                )
                self._session.add(discipline)
                generated_disciplines.append(discipline)

        await self._session.flush()

        for discipline_index, discipline in enumerate(generated_disciplines):
            entries_to_use = sample(athlete_names, k=min(len(athlete_names), payload.lanes))
            teams_cycle = sample(team_names, k=min(len(team_names), payload.lanes))
            for lane_number, (athlete, team) in enumerate(zip(entries_to_use, teams_cycle), start=1):
                entry_status = (
                    EventEntryStatus.FINISHED
                    if payload.include_results and discipline_index == 0
                    else EventEntryStatus.LIVE
                    if discipline.status == EventDisciplineStatus.LIVE
                    else EventEntryStatus.SCHEDULED
                )
                position = lane_number if entry_status == EventEntryStatus.FINISHED else None
                result = None
                points = None
                if entry_status == EventEntryStatus.FINISHED:
                    result = f"{10.2 + (lane_number * 0.07):.2f}s"
                    points = max(0, (payload.lanes - lane_number + 1) * 2)
                entry = EventEntry(
                    discipline_id=discipline.id,
                    athlete_name=athlete,
                    team_name=team,
                    lane=str(lane_range[lane_number - 1]),
                    bib=f"{discipline_index + 1:02d}{lane_number:02d}",
                    status=entry_status,
                    position=position,
                    result=result,
                    points=points,
                    notes="Demo entry",
                )
                self._session.add(entry)

        await self._session.commit()

        return await self.get_event_detail(event_id)


async def get_events_service(session: AsyncSession = Depends(get_session)) -> EventsService:
    return EventsService(session)
