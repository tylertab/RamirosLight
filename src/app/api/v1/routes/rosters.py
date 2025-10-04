from fastapi import APIRouter, Depends, status

from app.core.authorization import require_feature
from app.domain import SubscriptionFeature
from app.schemas.roster import RosterCreate, RosterRead
from app.schemas.user import UserRead
from app.services.rosters import RostersService, get_rosters_service

router = APIRouter(prefix="/rosters", tags=["rosters"])


@router.get("/", response_model=list[RosterRead])
async def list_rosters(service: RostersService = Depends(get_rosters_service)) -> list[RosterRead]:
    return await service.list_rosters()


@router.post("/", response_model=RosterRead, status_code=status.HTTP_201_CREATED)
async def create_roster(
    payload: RosterCreate,
    service: RostersService = Depends(get_rosters_service),
    current_user: UserRead = Depends(require_feature(SubscriptionFeature.ROSTER_MANAGEMENT)),
) -> RosterRead:
    return await service.create_roster(payload, owner_id=current_user.id)
