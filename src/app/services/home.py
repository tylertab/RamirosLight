"""Aggregated data helpers for the landing and live views."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Iterable

from fastapi import HTTPException
from sqlalchemy import select

from app.core.database import DatabaseSessionManager
from app.domain import SubscriptionTier
from app.models import Event, EventDiscipline, EventEntry, Federation, Roster
from app.schemas.event import (
    EventDetailRead,
    EventDisciplineRead,
    EventDisciplineStatus,
    EventEntryRead,
    EventEntryStatus,
    EventRead,
    EventSessionRead,
    EventSessionStatus,
)
from app.schemas.home import HomeClub, HomeFederation, HomeResult, HomeSnapshot
from app.schemas.news import NewsRead
from app.services.bootstrap import (
    SAMPLE_EVENTS,
    SAMPLE_FEDERATIONS,
    SAMPLE_NEWS,
    SAMPLE_RECENT_RESULTS,
)
from app.services.events import EventsService
from app.services.news import NewsService


def _fallback_events() -> list[EventRead]:
    return [
        EventRead(
            id=index,
            name=item["name"],
            location=item["location"],
            start_date=item["start_date"],
            end_date=item["end_date"],
            federation_id=item.get("federation_id"),
        )
        for index, item in enumerate(SAMPLE_EVENTS, start=1)
    ]


def _fallback_federations() -> list[HomeFederation]:
    federations: list[HomeFederation] = []
    for index, item in enumerate(SAMPLE_FEDERATIONS, start=1):
        clubs = [
            HomeClub(
                id=index * 100 + club_index,
                name=club["name"],
                country=club.get("country"),
                division=club.get("division"),
                coach_name=club.get("coach_name"),
                athlete_count=club.get("athlete_count"),
            )
            for club_index, club in enumerate(item.get("clubs", []), start=1)
        ]
        federations.append(
            HomeFederation(
                id=index,
                name=item["name"],
                country=item.get("country"),
                website=item.get("website"),
                clubs=clubs,
            )
        )
    return federations


def _fallback_recent_results() -> list[HomeResult]:
    now = datetime.now(tz=timezone.utc)
    return [
        HomeResult(
            entry_id=index,
            event_id=result["event_id"],
            event_name=result["event_name"],
            discipline_id=result["discipline_id"],
            discipline_name=result["discipline_name"],
            athlete_name=result["athlete_name"],
            team_name=result.get("team_name"),
            position=result.get("position"),
            result=result.get("result"),
            points=result.get("points"),
            roster_id=result.get("roster_id"),
            roster_name=result.get("roster_name"),
            federation_id=result.get("federation_id"),
            federation_name=result.get("federation_name"),
            updated_at=now - timedelta(minutes=index * 5),
        )
        for index, result in enumerate(SAMPLE_RECENT_RESULTS, start=1)
    ]


def _fallback_news() -> list[NewsRead]:
    now = datetime.now(tz=timezone.utc)
    return [
        NewsRead(
            id=index,
            title=item["title"],
            region=item["region"],
            excerpt=item.get("excerpt"),
            content=item["content"],
            audience=item["audience"],
            published_at=now - timedelta(days=index),
        )
        for index, item in enumerate(SAMPLE_NEWS, start=1)
    ]


def _fallback_event_detail(event_id: int = 1) -> EventDetailRead:
    now = datetime.now(tz=timezone.utc)
    start = (now - timedelta(days=1)).date()
    end = (now + timedelta(days=1)).date()

    session_one_start = now - timedelta(minutes=30)
    session_one_end = now + timedelta(hours=1)
    session_two_start = now + timedelta(hours=2)
    session_two_end = now + timedelta(hours=3)

    session_one = EventSessionRead(
        id=1,
        name="Morning Session",
        start_time=session_one_start,
        end_time=session_one_end,
        venue="Main Stadium",
        status=EventSessionStatus.LIVE,
        description="Sample data session",
    )
    session_two = EventSessionRead(
        id=2,
        name="Evening Finals",
        start_time=session_two_start,
        end_time=session_two_end,
        venue="Main Stadium",
        status=EventSessionStatus.SCHEDULED,
        description="Sample finals block",
    )

    sprint_entries = [
        EventEntryRead(
            id=1,
            athlete_name="Valentina Ríos",
            team_name="Andean Flyers",
            status=EventEntryStatus.FINISHED,
            lane="4",
            position=1,
            result="11.32s",
            points=12,
            notes="Demo entry",
            bib="0101",
            roster_id=None,
            roster=None,
            updated_at=now,
        ),
        EventEntryRead(
            id=2,
            athlete_name="Mateo Herrera",
            team_name="Caribbean Storm",
            status=EventEntryStatus.FINISHED,
            lane="5",
            position=2,
            result="11.40s",
            points=10,
            notes="Demo entry",
            bib="0102",
            roster_id=None,
            roster=None,
            updated_at=now,
        ),
        EventEntryRead(
            id=3,
            athlete_name="Camila Ibáñez",
            team_name="Patagonia Peaks",
            status=EventEntryStatus.FINISHED,
            lane="3",
            position=3,
            result="11.55s",
            points=8,
            notes="Demo entry",
            bib="0103",
            roster_id=None,
            roster=None,
            updated_at=now,
        ),
    ]

    long_jump_entries = [
        EventEntryRead(
            id=4,
            athlete_name="Renata Gómez",
            team_name="Cusco Distance",
            status=EventEntryStatus.LIVE,
            lane=None,
            position=None,
            result="6.48m",
            points=None,
            notes="Wind legal",
            bib="0201",
            roster_id=None,
            roster=None,
            updated_at=now,
        ),
        EventEntryRead(
            id=5,
            athlete_name="Daniel Torres",
            team_name="Granada Hurdlers",
            status=EventEntryStatus.LIVE,
            lane=None,
            position=None,
            result="6.30m",
            points=None,
            notes="",
            bib="0202",
            roster_id=None,
            roster=None,
            updated_at=now,
        ),
    ]

    relay_entries = [
        EventEntryRead(
            id=6,
            athlete_name="Pacífico Runners",
            team_name="Pacífico Runners",
            status=EventEntryStatus.SCHEDULED,
            lane="4",
            position=None,
            result=None,
            points=None,
            notes="",
            bib="0301",
            roster_id=None,
            roster=None,
            updated_at=now,
        ),
        EventEntryRead(
            id=7,
            athlete_name="Quito Relays",
            team_name="Quito Relays",
            status=EventEntryStatus.SCHEDULED,
            lane="5",
            position=None,
            result=None,
            points=None,
            notes="",
            bib="0302",
            roster_id=None,
            roster=None,
            updated_at=now,
        ),
    ]

    disciplines = [
        EventDisciplineRead(
            id=1,
            session_id=session_one.id,
            name="100m",
            category="Sprints",
            round_name="Final",
            scheduled_start=session_one_start,
            scheduled_end=session_one_start + timedelta(minutes=30),
            status=EventDisciplineStatus.FINALIZED,
            venue="Main Stadium",
            order=1,
            session=session_one,
            entries=sprint_entries,
        ),
        EventDisciplineRead(
            id=2,
            session_id=session_one.id,
            name="Long Jump",
            category="Jumps",
            round_name="Final",
            scheduled_start=session_one_start + timedelta(minutes=40),
            scheduled_end=session_one_start + timedelta(minutes=90),
            status=EventDisciplineStatus.LIVE,
            venue="Jumps Apron",
            order=2,
            session=session_one,
            entries=long_jump_entries,
        ),
        EventDisciplineRead(
            id=3,
            session_id=session_two.id,
            name="4x400m Relay",
            category="Relays",
            round_name="Final",
            scheduled_start=session_two_start,
            scheduled_end=session_two_start + timedelta(hours=1),
            status=EventDisciplineStatus.SCHEDULED,
            venue="Main Stadium",
            order=1,
            session=session_two,
            entries=relay_entries,
        ),
    ]

    return EventDetailRead(
        id=event_id,
        name="Aurora Indoor Classic",
        location="Oslo, Norway",
        start_date=start,
        end_date=end,
        federation_id=None,
        sessions=[session_one, session_two],
        disciplines=disciplines,
        latest_update=now,
    )


def _ensure_list(value: Iterable) -> list:
    return list(value) if value else []


async def get_home_snapshot() -> HomeSnapshot:
    session = DatabaseSessionManager().session()
    federations: list[HomeFederation] = []
    recent_results: list[HomeResult] = []
    try:
        events_service = EventsService(session)
        news_service = NewsService(session)

        events = await events_service.list_events()
        news = await news_service.list_articles(SubscriptionTier.FREE)

        federations_result = await session.execute(select(Federation))
        federation_entities = federations_result.scalars().all()

        club_rows = await session.execute(
            select(
                Federation.id.label("federation_id"),
                Roster.id.label("roster_id"),
                Roster.name.label("roster_name"),
                Roster.country,
                Roster.division,
                Roster.coach_name,
                Roster.athlete_count,
                EventEntry.team_name,
            )
            .select_from(EventEntry)
            .join(EventDiscipline, EventEntry.discipline_id == EventDiscipline.id)
            .join(Event, EventDiscipline.event_id == Event.id)
            .join(Federation, Event.federation_id == Federation.id)
            .outerjoin(Roster, EventEntry.roster_id == Roster.id)
        )

        clubs_by_federation: dict[int, dict[int | str, HomeClub]] = defaultdict(dict)
        for row in club_rows:
            name = row.roster_name or row.team_name
            if not name:
                continue
            key = row.roster_id or name
            if key in clubs_by_federation[row.federation_id]:
                continue
            clubs_by_federation[row.federation_id][key] = HomeClub(
                id=row.roster_id,
                name=name,
                country=row.country,
                division=row.division,
                coach_name=row.coach_name,
                athlete_count=row.athlete_count,
            )

        federations = [
            HomeFederation(
                id=federation.id,
                name=federation.name,
                country=federation.country,
                website=federation.website,
                clubs=list(clubs_by_federation.get(federation.id, {}).values()),
            )
            for federation in federation_entities
        ]

        recent_rows = await session.execute(
            select(
                EventEntry.id.label("entry_id"),
                EventEntry.updated_at,
                EventEntry.athlete_name,
                EventEntry.team_name,
                EventEntry.position,
                EventEntry.result,
                EventEntry.points,
                Event.id.label("event_id"),
                Event.name.label("event_name"),
                EventDiscipline.id.label("discipline_id"),
                EventDiscipline.name.label("discipline_name"),
                Federation.id.label("federation_id"),
                Federation.name.label("federation_name"),
                Roster.id.label("roster_id"),
                Roster.name.label("roster_name"),
            )
            .select_from(EventEntry)
            .join(EventDiscipline, EventEntry.discipline_id == EventDiscipline.id)
            .join(Event, EventDiscipline.event_id == Event.id)
            .outerjoin(Federation, Event.federation_id == Federation.id)
            .outerjoin(Roster, EventEntry.roster_id == Roster.id)
            .order_by(EventEntry.updated_at.desc())
            .limit(12)
        )

        recent_results = [
            HomeResult(
                entry_id=row.entry_id,
                event_id=row.event_id,
                event_name=row.event_name,
                discipline_id=row.discipline_id,
                discipline_name=row.discipline_name,
                athlete_name=row.athlete_name,
                team_name=row.team_name,
                position=row.position,
                result=row.result,
                points=row.points,
                roster_id=row.roster_id,
                roster_name=row.roster_name or row.team_name,
                federation_id=row.federation_id,
                federation_name=row.federation_name,
                updated_at=row.updated_at,
            )
            for row in recent_rows
        ]

        live_event: EventDetailRead | None = None
        for event in events:
            try:
                detail = await events_service.get_event_detail(event.id)
            except HTTPException:
                continue
            if detail.disciplines or detail.sessions:
                live_event = detail
                break
    finally:
        await session.close()

    events_list = _ensure_list(events) or _fallback_events()
    federations_list = federations or _fallback_federations()
    results_list = _ensure_list(recent_results) or _fallback_recent_results()
    news_list = _ensure_list(news) or _fallback_news()

    if live_event is None:
        first_event_id = events_list[0].id if events_list else 1
        live_event = _fallback_event_detail(first_event_id)

    return HomeSnapshot(
        federations=federations_list,
        events=events_list,
        recent_results=results_list,
        news=news_list,
        live_event=live_event,
    )


async def get_event_detail_snapshot(event_id: int) -> EventDetailRead:
    session = DatabaseSessionManager().session()
    try:
        events_service = EventsService(session)
        try:
            return await events_service.get_event_detail(event_id)
        except HTTPException:
            return _fallback_event_detail(event_id)
    finally:
        await session.close()
