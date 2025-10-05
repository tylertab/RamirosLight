from collections.abc import Iterable

from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Club, Event, EventDiscipline, EventEntry, Federation, Roster
from app.schemas.search import SearchResponse, SearchResult


class SearchService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def search(
        self,
        query: str,
        categories: Iterable[str],
    ) -> SearchResponse:
        normalized = {category.lower() for category in categories if category}
        if not normalized or "all" in normalized:
            normalized = {"federations", "clubs", "events", "results"}

        results: list[SearchResult] = []
        if "federations" in normalized:
            results.extend(await self._search_federations(query))
        if "clubs" in normalized:
            results.extend(await self._search_clubs(query))
        if "events" in normalized:
            results.extend(await self._search_events(query))
        if "results" in normalized:
            results.extend(await self._search_results(query))

        return SearchResponse(query=query, results=results)

    async def _search_federations(self, query: str) -> list[SearchResult]:
        stmt = (
            select(Federation)
            .where(
                or_(
                    Federation.name.ilike(f"%{query}%"),
                    Federation.country.ilike(f"%{query}%"),
                )
            )
            .limit(10)
        )
        result = await self._session.execute(stmt)
        federations = result.scalars().all()
        return [
            SearchResult(
                category="Federations",
                title=federation.name,
                subtitle=federation.country,
                detail=federation.website,
            )
            for federation in federations
        ]

    async def _search_clubs(self, query: str) -> list[SearchResult]:
        stmt = (
            select(Club, Federation)
            .join(Federation, Club.federation_id == Federation.id)
            .where(
                or_(
                    Club.name.ilike(f"%{query}%"),
                    Club.city.ilike(f"%{query}%"),
                    Club.country.ilike(f"%{query}%"),
                )
            )
            .limit(10)
        )
        result = await self._session.execute(stmt)
        rows = result.all()
        return [
            SearchResult(
                category="Clubs",
                title=club.name,
                subtitle=f"{club.city or club.country or ''}",
                detail=federation.name,
            )
            for club, federation in rows
        ]

    async def _search_events(self, query: str) -> list[SearchResult]:
        stmt = (
            select(Event)
            .where(
                or_(
                    Event.name.ilike(f"%{query}%"),
                    Event.location.ilike(f"%{query}%"),
                )
            )
            .limit(10)
        )
        result = await self._session.execute(stmt)
        events = result.scalars().all()
        return [
            SearchResult(
                category="Events",
                title=event.name,
                subtitle=event.location,
                detail=f"{event.start_date} – {event.end_date}",
            )
            for event in events
        ]

    async def _search_results(self, query: str) -> list[SearchResult]:
        stmt = (
            select(EventEntry, Event, EventDiscipline, Roster)
            .join(EventDiscipline, EventEntry.discipline_id == EventDiscipline.id)
            .join(Event, EventDiscipline.event_id == Event.id)
            .outerjoin(Roster, EventEntry.roster_id == Roster.id)
            .where(
                or_(
                    EventEntry.athlete_name.ilike(f"%{query}%"),
                    EventEntry.team_name.ilike(f"%{query}%"),
                    Event.name.ilike(f"%{query}%"),
                    EventDiscipline.name.ilike(f"%{query}%"),
                )
            )
            .order_by(EventEntry.updated_at.desc())
            .limit(10)
        )
        result = await self._session.execute(stmt)
        rows = result.all()
        return [
            SearchResult(
                category="Results",
                title=f"{entry.athlete_name} – {discipline.name}",
                subtitle=event.name,
                detail=entry.result or entry.team_name or (roster.name if roster else None),
            )
            for entry, event, discipline, roster in rows
        ]


async def get_search_service(session: AsyncSession = Depends(get_session)) -> SearchService:
    return SearchService(session)
