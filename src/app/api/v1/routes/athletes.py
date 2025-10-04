from fastapi import APIRouter, Depends

from fastapi import APIRouter, Depends

from app.core.authorization import require_feature
from app.domain import SubscriptionFeature
from app.schemas.athlete import AthleteHistoryResponse, AthleteProfileRead, AthleteProfileUpdate
from app.schemas.user import UserRead
from app.services.athletes import AthletesService, get_athletes_service

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.get("/{athlete_id}/history", response_model=AthleteHistoryResponse)
async def read_history(
    athlete_id: int,
    service: AthletesService = Depends(get_athletes_service),
    _: UserRead = Depends(require_feature(SubscriptionFeature.ATHLETE_HISTORY)),
) -> AthleteHistoryResponse:
    return await service.get_history(athlete_id)


@router.get("/{athlete_id}/profile", response_model=AthleteProfileRead)
async def read_profile(
    athlete_id: int,
    service: AthletesService = Depends(get_athletes_service),
    _: UserRead = Depends(require_feature(SubscriptionFeature.ATHLETE_HISTORY)),
) -> AthleteProfileRead:
    return await service.get_profile(athlete_id)


@router.put("/{athlete_id}/profile", response_model=AthleteProfileRead)
async def update_profile(
    athlete_id: int,
    payload: AthleteProfileUpdate,
    service: AthletesService = Depends(get_athletes_service),
    _: UserRead = Depends(require_feature(SubscriptionFeature.ROSTER_MANAGEMENT)),
) -> AthleteProfileRead:
    return await service.update_profile(athlete_id, payload)
