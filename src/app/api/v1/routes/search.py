from fastapi import APIRouter, Depends, Query

from app.schemas.search import SearchResponse
from app.services.search import SearchService, get_search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=SearchResponse)
async def global_search(
    query: str = Query(..., min_length=2, description="Query string to search across Trackeo"),
    categories: list[str] = Query(
        default=["all"],
        description="Categories to include (events, federations, clubs, news, results)",
    ),
    service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    return await service.search(query, categories)
