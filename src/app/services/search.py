from collections.abc import Iterable

from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Event, Federation, NewsArticle, Roster
from app.schemas.result import ResultSummary
from app.schemas.search import SearchResponse, SearchResult
from app.services.results import ResultsService


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
            normalized = {"events", "federations", "clubs", "news", "results"}

        results: list[SearchResult] = []
        if "events" in normalized:
            results.extend(await self._search_events(query))
        if "federations" in normalized:
            results.extend(await self._search_federations(query))
        if "clubs" in normalized:
            results.extend(await self._search_clubs(query))
        if "news" in normalized:
            results.extend(await self._search_news(query))
        if "results" in normalized:
            results.extend(await self._search_results(query))

        return SearchResponse(query=query, results=results)

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
            select(Roster)
            .where(
                or_(
                    Roster.name.ilike(f"%{query}%"),
                    Roster.country.ilike(f"%{query}%"),
                    Roster.coach_name.ilike(f"%{query}%"),
                )
            )
            .limit(10)
        )
        result = await self._session.execute(stmt)
        rosters = result.scalars().all()
        return [
            SearchResult(
                category="Clubs",
                title=roster.name,
                subtitle=f"{roster.country} · {roster.division}",
                detail=f"{roster.athlete_count} athletes",
            )
            for roster in rosters
        ]

    async def _search_news(self, query: str) -> list[SearchResult]:
        stmt = (
            select(NewsArticle)
            .where(
                or_(
                    NewsArticle.title.ilike(f"%{query}%"),
                    NewsArticle.region.ilike(f"%{query}%"),
                    NewsArticle.excerpt.ilike(f"%{query}%"),
                )
            )
            .limit(10)
        )
        result = await self._session.execute(stmt)
        articles = result.scalars().all()
        return [
            SearchResult(
                category="News",
                title=article.title,
                subtitle=article.region,
                detail=article.published_at.date().isoformat(),
            )
            for article in articles
        ]

    async def _search_results(self, query: str) -> list[SearchResult]:
        service = ResultsService(self._session)
        summaries: list[ResultSummary] = await service.search(query)
        return [
            SearchResult(
                category="Results",
                title=f"{summary.athlete_name} · {summary.result or 'Pending'}",
                subtitle=f"{summary.event_name} — {summary.discipline_name}",
                detail=summary.event_location,
            )
            for summary in summaries
        ]


async def get_search_service(session: AsyncSession = Depends(get_session)) -> SearchService:
    return SearchService(session)
