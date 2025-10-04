"""Endpoints that deliver aggregated demo data for the web front-end."""

from fastapi import APIRouter

from app.schemas.home import HomeSnapshot
from app.services.home import get_home_snapshot

router = APIRouter(prefix="/bootstrap", tags=["bootstrap"])


@router.get("/home", response_model=HomeSnapshot)
async def read_home_snapshot() -> HomeSnapshot:
    """Return a snapshot of athletes, events, rosters, and news for the home view."""

    return await get_home_snapshot()
