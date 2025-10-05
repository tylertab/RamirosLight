from fastapi import APIRouter, Depends, HTTPException, status

from app.core.authorization import require_roles
from app.schemas.federation import FederationSubmissionCreate, FederationSubmissionRead
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
