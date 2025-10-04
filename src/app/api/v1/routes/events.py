from fastapi import APIRouter, Depends

from app.schemas.event import EventCreate, EventRead
from app.services.events import EventsService, get_events_service

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventRead)
async def create_event(
    payload: EventCreate, service: EventsService = Depends(get_events_service)
) -> EventRead:
    return await service.create_event(payload)


@router.get("/", response_model=list[EventRead])
async def list_events(service: EventsService = Depends(get_events_service)) -> list[EventRead]:
    return await service.list_events()
