from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Event
from app.schemas.event import EventCreate, EventRead


class EventsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

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


async def get_events_service(session: AsyncSession = Depends(get_session)) -> EventsService:
    return EventsService(session)
