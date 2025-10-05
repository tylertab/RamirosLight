from fastapi import APIRouter, Depends, status

from app.core.authorization import get_current_user_with_model
from app.schemas.news import NewsCreate, NewsRead
from app.schemas.user import UserRead
from app.services.news import NewsService, get_news_service

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/", response_model=list[NewsRead])
async def list_news(
    service: NewsService = Depends(get_news_service),
) -> list[NewsRead]:
    return await service.list_articles()


@router.post("/", response_model=NewsRead, status_code=status.HTTP_201_CREATED)
async def publish_article(
    payload: NewsCreate,
    service: NewsService = Depends(get_news_service),
    _: UserRead = Depends(get_current_user_with_model),
) -> NewsRead:
    return await service.publish(payload)
