from fastapi import APIRouter, Depends, HTTPException, status

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.authorization import require_feature, require_roles
from app.domain import SubscriptionFeature
from app.schemas.federation import FederationSubmissionCreate, FederationSubmissionRead
from app.schemas.user import UserRead
from app.services.federations import FederationIngestionService, get_federation_service

router = APIRouter(prefix="/federations", tags=["federations"])


@router.post(
    "/submissions",
    response_model=FederationSubmissionRead,
    status_code=status.HTTP_202_ACCEPTED,
)
async def submit_results(
    payload: FederationSubmissionCreate,
    service: FederationIngestionService = Depends(get_federation_service),
    _: UserRead = Depends(require_roles("federation")),
    __: UserRead = Depends(require_feature(SubscriptionFeature.FEDERATION_UPLOAD)),
) -> FederationSubmissionRead:
    try:
        return await service.enqueue_submission(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get(
    "/submissions",
    response_model=list[FederationSubmissionRead],
    dependencies=[Depends(require_roles("federation"))],
)
async def list_submissions(
    service: FederationIngestionService = Depends(get_federation_service),
) -> list[FederationSubmissionRead]:
    return await service.list_submissions()
