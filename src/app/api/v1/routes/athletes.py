from fastapi import APIRouter, Depends

from app.core.authorization import get_current_user_with_model
from app.schemas.athlete import (
    AthleteDetail,
    AthleteHistoryResponse,
    AthleteProfileRead,
    AthleteProfileUpdate,
)
from app.schemas.user import UserRead
from app.services.athletes import AthletesService, get_athletes_service

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.get("/{athlete_id}", response_model=AthleteDetail)
async def read_detail(
    athlete_id: int,
    service: AthletesService = Depends(get_athletes_service),
) -> AthleteDetail:
    return await service.get_detail(athlete_id)


@router.get("/{athlete_id}/history", response_model=AthleteHistoryResponse)
async def read_history(
    athlete_id: int,
    service: AthletesService = Depends(get_athletes_service),
) -> AthleteHistoryResponse:
    return await service.get_history(athlete_id)


@router.get("/{athlete_id}/profile", response_model=AthleteProfileRead)
async def read_profile(
    athlete_id: int,
    service: AthletesService = Depends(get_athletes_service),
) -> AthleteProfileRead:
    return await service.get_profile(athlete_id)


@router.put("/{athlete_id}/profile", response_model=AthleteProfileRead)
async def update_profile(
    athlete_id: int,
    payload: AthleteProfileUpdate,
    service: AthletesService = Depends(get_athletes_service),
    _: UserRead = Depends(get_current_user_with_model),
) -> AthleteProfileRead:
    return await service.update_profile(athlete_id, payload)
