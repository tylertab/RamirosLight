"""Utilities for seeding demo data during application startup."""

from __future__ import annotations

from datetime import date, datetime, time, timezone

from sqlalchemy import select

from app.core.config import SettingsSingleton
from app.core.database import DatabaseSessionManager
from app.models import Event, Federation, NewsArticle, NewsAudience, Roster, User
from app.schemas.event import EventCreate, EventFakeTimelineRequest
from app.schemas.user import UserCreate
from app.services.accounts import AccountsService
from app.services.events import EventsService

SAMPLE_USERS: list[dict[str, str]] = [
    {
        "full_name": "Ramiro Lightfoot",
        "email": "ramiro.lightfoot@example.com",
        "role": "athlete",
        "password": "Shimmering123",
    },
    {
        "full_name": "Sofía Delgado",
        "email": "sofia.delgado@example.com",
        "role": "athlete",
        "password": "Sprinter123",
    },
    {
        "full_name": "Liam O'Connor",
        "email": "liam.oconnor@example.com",
        "role": "athlete",
        "password": "Hurdles123",
    },
]

SAMPLE_EVENTS: list[dict[str, object]] = [
    {
        "name": "Aurora Indoor Classic",
        "location": "Oslo, Norway",
        "start_date": date(2024, 2, 10),
        "end_date": date(2024, 2, 12),
        "federation_id": None,
        "seed_demo": True,
    },
    {
        "name": "Sunset Coast Invitational",
        "location": "Porto, Portugal",
        "start_date": date(2024, 4, 22),
        "end_date": date(2024, 4, 24),
        "federation_id": None,
    },
    {
        "name": "Highlands Distance Festival",
        "location": "Edinburgh, Scotland",
        "start_date": date(2024, 9, 14),
        "end_date": date(2024, 9, 15),
        "federation_id": None,
    },
]

SAMPLE_ROSTERS: list[dict[str, object]] = [
    {
        "name": "Club Andino Quito",
        "country": "Ecuador",
        "division": "U20",
        "coach_name": "María Torres",
        "athlete_count": 18,
        "owner_email": "ramiro.lightfoot@example.com",
    },
    {
        "name": "São Paulo Relays",
        "country": "Brazil",
        "division": "Senior",
        "coach_name": "João Pereira",
        "athlete_count": 24,
        "owner_email": "sofia.delgado@example.com",
    },
    {
        "name": "Buenos Aires Elite",
        "country": "Argentina",
        "division": "Senior",
        "coach_name": "Lucía Fernández",
        "athlete_count": 22,
        "owner_email": "liam.oconnor@example.com",
    },
]

SAMPLE_FEDERATIONS: list[dict[str, object]] = [
    {
        "name": "Confederación Atlética Andina",
        "country": "Ecuador",
        "website": "https://anda-athletics.example.com",
    },
    {
        "name": "Federação Paulista de Atletismo",
        "country": "Brazil",
        "website": "https://fpa.example.br",
    },
    {
        "name": "Federación Atlética Metropolitana",
        "country": "Argentina",
        "website": "https://fam.example.ar",
    },
]

SAMPLE_NEWS: list[dict[str, object]] = [
    {
        "title": "Trackeo launches bilingual live splits across South America",
        "region": "Latin America",
        "excerpt": "Federations gain instant insights with localized dashboards in Spanish and Portuguese.",
        "content": "Trackeo now synchronizes live splits from Rio to Bogotá, unlocking analytics for every federation.",
        "audience": NewsAudience.PUBLIC,
    },
    {
        "title": "Altitude training hub opens in Quito",
        "region": "Ecuador",
        "excerpt": "National squads gather for the final pre-Pan American training camp.",
        "content": "The Ecuadorian federation partnered with Trackeo to monitor training loads and readiness ahead of the Pan American Games.",
        "audience": NewsAudience.PREMIUM,
    },
    {
        "title": "Coach insights: Building world-class relays",
        "region": "Brazil",
        "excerpt": "Strategies from São Paulo Relays as they prep for the Golden Night showcase.",
        "content": "Head coach João Pereira shares how video analysis and precise exchange metrics drive the squad's consistency.",
        "audience": NewsAudience.COACH,
    },
]


async def seed_initial_data() -> None:
    """Populate the database with demo content if core tables are empty."""

    settings = SettingsSingleton().instance
    if not settings.seed_demo_data:
        return

    session = DatabaseSessionManager().session()
    try:
        accounts_service = AccountsService(session)
        events_service = EventsService(session)

        user_ids: dict[str, int] = {}
        for sample in SAMPLE_USERS:
            existing = await accounts_service.get_user_by_email(sample["email"])
            if existing is None:
                created = await accounts_service.create_user(UserCreate(**sample))
                user_ids[created.email] = created.id
            else:
                user_ids[existing.email] = existing.id

        if not user_ids:
            result = await session.execute(select(User.email, User.id))
            for email, user_id in result.all():
                user_ids[email] = user_id

        rosters_added = False
        for sample in SAMPLE_ROSTERS:
            roster_data = dict(sample)
            owner_email = roster_data.pop("owner_email", None)
            owner_id = user_ids.get(owner_email) if owner_email else None
            exists = await session.execute(
                select(Roster.id).where(Roster.name == roster_data["name"])
            )
            if exists.scalar_one_or_none() is not None:
                continue
            roster = Roster(owner_id=owner_id, **roster_data)
            session.add(roster)
            rosters_added = True

        events_seeded = False
        for sample in SAMPLE_EVENTS:
            exists = await session.execute(
                select(Event.id).where(Event.name == sample["name"])
            )
            if exists.scalar_one_or_none() is not None:
                continue
            payload = EventCreate(
                name=sample["name"],
                location=sample["location"],
                start_date=sample["start_date"],
                end_date=sample["end_date"],
                federation_id=sample.get("federation_id"),
            )
            created = await events_service.create_event(payload)
            events_seeded = True
            if sample.get("seed_demo"):
                start_anchor = datetime.combine(
                    payload.start_date,
                    time(hour=9, minute=0),
                    tzinfo=timezone.utc,
                )
                await events_service.generate_fake_timeline(
                    created.id,
                    EventFakeTimelineRequest(
                        start_time=start_anchor,
                        sessions=3,
                        disciplines_per_session=3,
                        lanes=8,
                        include_results=True,
                    ),
                )

        federations_added = False
        for sample in SAMPLE_FEDERATIONS:
            exists = await session.execute(
                select(Federation.id).where(Federation.name == sample["name"])
            )
            if exists.scalar_one_or_none() is not None:
                continue
            federation = Federation(**sample)
            session.add(federation)
            federations_added = True

        news_added = False
        for sample in SAMPLE_NEWS:
            exists = await session.execute(
                select(NewsArticle.id).where(NewsArticle.title == sample["title"])
            )
            if exists.scalar_one_or_none() is not None:
                continue
            article = NewsArticle(
                title=sample["title"],
                region=sample["region"],
                excerpt=sample["excerpt"],
                content=sample["content"],
                audience=sample["audience"],
                published_at=datetime.now(tz=timezone.utc),
            )
            session.add(article)
            news_added = True

        if rosters_added or news_added or events_seeded:
            await session.commit()
    finally:
        await session.close()
