from fastapi import APIRouter, Depends, HTTPException, status

from app.core.authorization import get_current_user_with_model
from app.schemas.subscription import (
    SubscriptionPlanRead,
    SubscriptionStatusRead,
    SubscriptionUpgradeRequest,
)
from app.schemas.user import UserRead
from app.services.accounts import AccountsService, get_accounts_service
from app.services.subscriptions import SubscriptionService, get_subscription_service

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/plans", response_model=list[SubscriptionPlanRead])
async def list_plans(service: SubscriptionService = Depends(get_subscription_service)) -> list[SubscriptionPlanRead]:
    return [SubscriptionPlanRead.from_plan(plan) for plan in service.plans()]


@router.get("/status", response_model=SubscriptionStatusRead)
async def read_status(current_user: UserRead = Depends(get_current_user_with_model)) -> SubscriptionStatusRead:
    return SubscriptionStatusRead(
        tier=current_user.subscription_tier,
        expires_at=current_user.subscription_expires_at,
        started_at=current_user.subscription_started_at,
    )


@router.post("/upgrade", response_model=SubscriptionStatusRead)
async def upgrade_subscription(
    payload: SubscriptionUpgradeRequest,
    current_user: UserRead = Depends(get_current_user_with_model),
    accounts: AccountsService = Depends(get_accounts_service),
) -> SubscriptionStatusRead:
    user_model = await accounts.get_user_model(current_user.id)
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not found")
    upgraded = await accounts.upgrade_subscription(
        user_model,
        payload.tier,
        payload.duration_days,
        payload.payment_reference,
    )
    return SubscriptionStatusRead(
        tier=upgraded.subscription_tier,
        expires_at=upgraded.subscription_expires_at,
        started_at=upgraded.subscription_started_at,
    )
