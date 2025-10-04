"""Aggregated data helpers for the landing and live views."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from fastapi import HTTPException

from app.core.database import DatabaseSessionManager
from app.domain import SubscriptionTier
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
from app.schemas.home import HomeSnapshot
from app.schemas.news import NewsRead
from app.schemas.roster import RosterRead
from app.schemas.user import UserRead
from app.services.accounts import AccountsService
from app.services.bootstrap import (
    SAMPLE_EVENTS,
    SAMPLE_NEWS,
    SAMPLE_ROSTERS,
    SAMPLE_USERS,
)
from app.services.events import EventsService
from app.services.news import NewsService
from app.services.rosters import RostersService


def _fallback_athletes() -> list[UserRead]:
    now = datetime.now(tz=timezone.utc)
    base_started = now - timedelta(days=3)
    return [
        UserRead(
            id=index,
            email=item["email"],
            full_name=item["full_name"],
            role=item["role"],
            subscription_tier=SubscriptionTier.FREE,
            created_at=now - timedelta(days=index),
            subscription_started_at=base_started,
            subscription_expires_at=base_started + timedelta(days=30),
        )
        for index, item in enumerate(SAMPLE_USERS, start=1)
    ]


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


def _fallback_rosters() -> list[RosterRead]:
    now = datetime.now(tz=timezone.utc)
    return [
        RosterRead(
            id=index,
            name=item["name"],
            country=item["country"],
            division=item["division"],
            coach_name=item["coach_name"],
            athlete_count=item.get("athlete_count", 0),
            updated_at=now - timedelta(days=index),
        )
        for index, item in enumerate(SAMPLE_ROSTERS, start=1)
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
    try:
        accounts_service = AccountsService(session)
        events_service = EventsService(session)
        rosters_service = RostersService(session)
        news_service = NewsService(session)

        athletes = await accounts_service.list_users()
        events = await events_service.list_events()
        rosters = await rosters_service.list_rosters()
        news = await news_service.list_articles(SubscriptionTier.FREE)

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

    athletes_list = _ensure_list(athletes) or _fallback_athletes()
    events_list = _ensure_list(events) or _fallback_events()
    rosters_list = _ensure_list(rosters) or _fallback_rosters()
    news_list = _ensure_list(news) or _fallback_news()

    if live_event is None:
        first_event_id = events_list[0].id if events_list else 1
        live_event = _fallback_event_detail(first_event_id)

    return HomeSnapshot(
        athletes=athletes_list,
        events=events_list,
        rosters=rosters_list,
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
