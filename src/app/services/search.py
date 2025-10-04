from collections.abc import Iterable

from fastapi import Depends
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain import SubscriptionTier
from app.models import Event, NewsArticle, NewsAudience, Roster, User
from app.schemas.search import SearchResponse, SearchResult


class SearchService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def search(
        self,
        query: str,
        categories: Iterable[str],
        tier: SubscriptionTier,
    ) -> SearchResponse:
        normalized = {category.lower() for category in categories if category}
        if not normalized or "all" in normalized:
            normalized = {"athletes", "events", "rosters", "news"}

        results: list[SearchResult] = []
        if "athletes" in normalized:
            results.extend(await self._search_athletes(query))
        if "events" in normalized:
            results.extend(await self._search_events(query))
        if "rosters" in normalized:
            results.extend(await self._search_rosters(query))
        if "news" in normalized:
            results.extend(await self._search_news(query, tier))

        return SearchResponse(query=query, results=results)

    async def _search_athletes(self, query: str) -> list[SearchResult]:
        stmt = (
            select(User)
            .where(User.role == "athlete")
            .where(
                or_(
                    User.full_name.ilike(f"%{query}%"),
                    User.email.ilike(f"%{query}%"),
                )
            )
            .limit(10)
        )
        result = await self._session.execute(stmt)
        athletes = result.scalars().all()
        return [
            SearchResult(
                category="Athletes",
                title=athlete.full_name,
                subtitle=athlete.email,
                detail=athlete.subscription_tier.value,
            )
            for athlete in athletes
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

    async def _search_rosters(self, query: str) -> list[SearchResult]:
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
                category="Rosters",
                title=roster.name,
                subtitle=f"{roster.country} · {roster.division}",
                detail=f"{roster.athlete_count} athletes",
            )
            for roster in rosters
        ]

    async def _search_news(self, query: str, tier: SubscriptionTier) -> list[SearchResult]:
        audiences = [NewsAudience.PUBLIC]
        if tier.meets(SubscriptionTier.PREMIUM):
            audiences.append(NewsAudience.PREMIUM)
        if tier.meets(SubscriptionTier.COACH):
            audiences.append(NewsAudience.COACH)
        stmt = (
            select(NewsArticle)
            .where(NewsArticle.audience.in_(audiences))
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


async def get_search_service(session: AsyncSession = Depends(get_session)) -> SearchService:
    return SearchService(session)
