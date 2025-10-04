from fastapi import APIRouter, Depends

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
from app.services.events import EventsService, get_events_service

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventRead, status_code=201)
async def create_event(
    payload: EventCreate, service: EventsService = Depends(get_events_service)
) -> EventRead:
    return await service.create_event(payload)


@router.get("/", response_model=list[EventRead])
async def list_events(service: EventsService = Depends(get_events_service)) -> list[EventRead]:
    return await service.list_events()


@router.get("/{event_id}", response_model=EventDetailRead)
async def read_event_detail(
    event_id: int, service: EventsService = Depends(get_events_service)
) -> EventDetailRead:
    return await service.get_event_detail(event_id)


@router.post("/{event_id}/sessions", response_model=EventSessionRead, status_code=201)
async def create_event_session(
    event_id: int,
    payload: EventSessionCreate,
    service: EventsService = Depends(get_events_service),
) -> EventSessionRead:
    return await service.create_session(event_id, payload)


@router.post("/{event_id}/disciplines", response_model=EventDisciplineRead, status_code=201)
async def create_event_discipline(
    event_id: int,
    payload: EventDisciplineCreate,
    service: EventsService = Depends(get_events_service),
) -> EventDisciplineRead:
    return await service.create_discipline(event_id, payload)


@router.post(
    "/disciplines/{discipline_id}/entries",
    response_model=EventEntryRead,
    status_code=201,
)
async def create_event_entry(
    discipline_id: int,
    payload: EventEntryCreate,
    service: EventsService = Depends(get_events_service),
) -> EventEntryRead:
    return await service.create_entry(discipline_id, payload)


@router.patch("/entries/{entry_id}", response_model=EventEntryRead)
async def update_event_entry(
    entry_id: int,
    payload: EventEntryUpdate,
    service: EventsService = Depends(get_events_service),
) -> EventEntryRead:
    return await service.update_entry(entry_id, payload)


@router.post("/{event_id}/demo", response_model=EventDetailRead)
async def generate_event_demo(
    event_id: int,
    payload: EventFakeTimelineRequest,
    service: EventsService = Depends(get_events_service),
) -> EventDetailRead:
    return await service.generate_fake_timeline(event_id, payload)
