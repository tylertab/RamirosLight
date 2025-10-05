"""Utilities for seeding demo data during application startup."""

from __future__ import annotations

from datetime import date, datetime, time, timezone
from hashlib import sha256

from sqlalchemy import select

from app.core.config import SettingsSingleton
from app.core.database import DatabaseSessionManager
from app.models import Club, Event, Federation, NewsArticle, NewsAudience, Roster
from app.schemas.event import EventCreate, EventFakeTimelineRequest
from app.services.events import EventsService

SAMPLE_FEDERATIONS: list[dict[str, object]] = [
    {
        "name": "Federación Atlética Sudamericana",
        "country": "Argentina",
        "website": "https://fas.example.org",
        "token": "fas-demo-token",
        "clubs": [
            {
                "name": "Patagonia Peaks",
                "city": "Bariloche",
                "country": "Argentina",
                "rosters": [
                    {
                        "division": "Senior",
                        "coach_name": "Lucía Fernández",
                        "athlete_count": 22,
                    }
                ],
            },
            {
                "name": "Buenos Aires Elite",
                "city": "Buenos Aires",
                "country": "Argentina",
                "rosters": [
                    {
                        "division": "Senior",
                        "coach_name": "Mariano Silva",
                        "athlete_count": 18,
                    }
                ],
            },
        ],
    },
    {
        "name": "Confederación Andina de Atletismo",
        "country": "Ecuador",
        "website": "https://caa.example.org",
        "token": "caa-demo-token",
        "clubs": [
            {
                "name": "Andean Flyers",
                "city": "Quito",
                "country": "Ecuador",
                "rosters": [
                    {
                        "division": "U20",
                        "coach_name": "María Torres",
                        "athlete_count": 20,
                    }
                ],
            },
            {
                "name": "Cusco Distance",
                "city": "Cusco",
                "country": "Peru",
                "rosters": [
                    {
                        "division": "Senior",
                        "coach_name": "Renato Medina",
                        "athlete_count": 16,
                    }
                ],
            },
        ],
    },
    {
        "name": "Liga Atlética do Atlântico",
        "country": "Brazil",
        "website": "https://laa.example.org",
        "token": "laa-demo-token",
        "clubs": [
            {
                "name": "São Paulo Relays",
                "city": "São Paulo",
                "country": "Brazil",
                "rosters": [
                    {
                        "division": "Senior",
                        "coach_name": "João Pereira",
                        "athlete_count": 24,
                    }
                ],
            },
            {
                "name": "Granada Hurdlers",
                "city": "Granada",
                "country": "Spain",
                "rosters": [
                    {
                        "division": "Senior",
                        "coach_name": "Irene Martínez",
                        "athlete_count": 21,
                    }
                ],
            },
        ],
    },
]

SAMPLE_EVENTS: list[dict[str, object]] = [
    {
        "name": "Aurora Indoor Classic",
        "location": "Oslo, Norway",
        "start_date": date(2024, 2, 10),
        "end_date": date(2024, 2, 12),
        "federation": "Confederación Andina de Atletismo",
        "seed_demo": True,
    },
    {
        "name": "Sunset Coast Invitational",
        "location": "Porto, Portugal",
        "start_date": date(2024, 4, 22),
        "end_date": date(2024, 4, 24),
        "federation": "Liga Atlética do Atlântico",
    },
    {
        "name": "Highlands Distance Festival",
        "location": "Edinburgh, Scotland",
        "start_date": date(2024, 9, 14),
        "end_date": date(2024, 9, 15),
        "federation": "Federación Atlética Sudamericana",
    },
]

SAMPLE_RECENT_RESULTS: list[dict[str, object]] = [
    {
        "event_id": 1,
        "event_name": "Aurora Indoor Classic",
        "discipline_id": 1,
        "discipline_name": "100m Final",
        "athlete_name": "Valentina Ríos",
        "team_name": "Andean Flyers",
        "position": 1,
        "result": "11.32",
        "points": 12,
        "federation_id": 2,
        "federation_name": "Confederación Andina de Atletismo",
        "roster_name": "Andean Flyers",
        "club_name": "Andean Flyers",
    },
    {
        "event_id": 1,
        "event_name": "Aurora Indoor Classic",
        "discipline_id": 2,
        "discipline_name": "Long Jump",
        "athlete_name": "Renata Gómez",
        "team_name": "Cusco Distance",
        "position": 2,
        "result": "6.48",
        "points": 9,
        "federation_id": 2,
        "federation_name": "Confederación Andina de Atletismo",
        "roster_name": "Cusco Distance",
        "club_name": "Cusco Distance",
    },
    {
        "event_id": 2,
        "event_name": "Sunset Coast Invitational",
        "discipline_id": 3,
        "discipline_name": "4x400m Relay",
        "athlete_name": "São Paulo Relays",
        "team_name": "São Paulo Relays",
        "position": 1,
        "result": "3:16.40",
        "points": 14,
        "federation_id": 3,
        "federation_name": "Liga Atlética do Atlântico",
        "roster_name": "São Paulo Relays",
        "club_name": "São Paulo Relays",
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
        events_service = EventsService(session)

        federation_ids: dict[str, int] = {}
        federations_added = False
        clubs_added = False
        rosters_added = False
        for sample in SAMPLE_FEDERATIONS:
            result = await session.execute(
                select(Federation).where(Federation.name == sample["name"])
            )
            federation = result.scalar_one_or_none()
            if federation is None:
                federation = Federation(
                    name=sample["name"],
                    country=sample.get("country"),
                    website=sample.get("website"),
                    ingest_token_hash=sha256(sample.get("token", "").encode("utf-8")).hexdigest()
                    if sample.get("token")
                    else None,
                )
                session.add(federation)
                await session.flush()
                federations_added = True
            elif sample.get("token"):
                federation.ingest_token_hash = sha256(sample["token"].encode("utf-8")).hexdigest()
                session.add(federation)
            federation_ids[federation.name] = federation.id

            for club_sample in sample.get("clubs", []):
                club_result = await session.execute(
                    select(Club).where(Club.name == club_sample["name"])
                )
                club = club_result.scalar_one_or_none()
                if club is None:
                    club = Club(
                        name=club_sample["name"],
                        city=club_sample.get("city"),
                        country=club_sample.get("country", sample.get("country")),
                        federation_id=federation.id,
                    )
                    session.add(club)
                    await session.flush()
                    clubs_added = True

                for roster_sample in club_sample.get("rosters", []):
                    roster_name = roster_sample.get("name", club_sample["name"])
                    exists = await session.execute(
                        select(Roster.id).where(Roster.name == roster_name)
                    )
                    if exists.scalar_one_or_none() is not None:
                        continue
                    roster = Roster(
                        name=roster_name,
                        country=club_sample.get("country", sample.get("country") or ""),
                        division=roster_sample.get("division", "Senior"),
                        coach_name=roster_sample.get("coach_name", "Trackeo Coach"),
                        athlete_count=roster_sample.get("athlete_count", 0),
                        club_id=club.id,
                    )
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
                federation_id=federation_ids.get(sample.get("federation")),
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

        if federations_added or clubs_added or rosters_added or news_added:
            await session.commit()
    finally:
        await session.close()
