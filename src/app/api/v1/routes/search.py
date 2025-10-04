from fastapi import APIRouter, Depends, Query

from app.core.security import get_optional_user
from app.domain import SubscriptionTier
from app.schemas.search import SearchResponse
from app.schemas.user import UserRead
from app.services.search import SearchService, get_search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=SearchResponse)
async def global_search(
    query: str = Query(..., min_length=2, description="Query string to search across Trackeo"),
    categories: list[str] = Query(default=["all"], description="Categories to include"),
    service: SearchService = Depends(get_search_service),
    current_user: UserRead | None = Depends(get_optional_user),
) -> SearchResponse:
    tier = current_user.subscription_tier if current_user else SubscriptionTier.FREE
    return await service.search(query, categories, tier)
