from fastapi import APIRouter, Depends, status

from app.schemas.subscriber import EmailSubscriberCreate, EmailSubscriberRead
from app.services.subscribers import (
    EmailSubscriptionService,
    get_email_subscription_service,
)

router = APIRouter(prefix="/subscribers", tags=["subscribers"])


@router.post("/", response_model=EmailSubscriberRead, status_code=status.HTTP_201_CREATED)
async def subscribe(
    payload: EmailSubscriberCreate,
    service: EmailSubscriptionService = Depends(get_email_subscription_service),
) -> EmailSubscriberRead:
    return await service.subscribe(payload)
