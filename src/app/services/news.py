from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain import SubscriptionTier
from app.models import NewsArticle, NewsAudience
from app.schemas.news import NewsCreate, NewsRead


class NewsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def publish(self, payload: NewsCreate) -> NewsRead:
        published_at = payload.published_at or datetime.now(tz=timezone.utc)
        article = NewsArticle(
            title=payload.title,
            region=payload.region,
            excerpt=payload.excerpt,
            content=payload.content,
            audience=payload.audience,
            published_at=published_at,
        )
        self._session.add(article)
        await self._session.commit()
        await self._session.refresh(article)
        return NewsRead.model_validate(article)

    async def list_articles(self, tier: SubscriptionTier) -> list[NewsRead]:
        allowed = self._allowed_audiences(tier)
        result = await self._session.execute(
            select(NewsArticle)
            .where(NewsArticle.audience.in_(allowed))
            .order_by(NewsArticle.published_at.desc())
        )
        articles = result.scalars().all()
        return [NewsRead.model_validate(item) for item in articles]

    def _allowed_audiences(self, tier: SubscriptionTier) -> list[NewsAudience]:
        allowed = [NewsAudience.PUBLIC]
        if tier.meets(SubscriptionTier.PREMIUM):
            allowed.append(NewsAudience.PREMIUM)
        if tier.meets(SubscriptionTier.COACH):
            allowed.append(NewsAudience.COACH)
        return allowed


async def get_news_service(session: AsyncSession = Depends(get_session)) -> NewsService:
    return NewsService(session)
