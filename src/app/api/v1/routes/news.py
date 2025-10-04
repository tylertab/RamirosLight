from fastapi import APIRouter, Depends, status

from app.core.authorization import require_feature
from app.core.security import get_optional_user
from app.domain import SubscriptionFeature, SubscriptionTier
from app.schemas.news import NewsCreate, NewsRead
from app.schemas.user import UserRead
from app.services.news import NewsService, get_news_service

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/", response_model=list[NewsRead])
async def list_news(
    service: NewsService = Depends(get_news_service),
    current_user: UserRead | None = Depends(get_optional_user),
) -> list[NewsRead]:
    tier = current_user.subscription_tier if current_user else SubscriptionTier.FREE
    return await service.list_articles(tier)


@router.post("/", response_model=NewsRead, status_code=status.HTTP_201_CREATED)
async def publish_article(
    payload: NewsCreate,
    service: NewsService = Depends(get_news_service),
    _: UserRead = Depends(require_feature(SubscriptionFeature.ROSTER_MANAGEMENT)),
) -> NewsRead:
    return await service.publish(payload)
