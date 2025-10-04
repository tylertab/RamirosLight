from datetime import datetime

from pydantic import BaseModel, Field

from app.domain import SubscriptionFeature, SubscriptionPlan, SubscriptionTier


class SubscriptionPlanRead(BaseModel):
    tier: SubscriptionTier
    price: float
    currency: str
    features: list[SubscriptionFeature]
    description: str

    @classmethod
    def from_plan(cls, plan: SubscriptionPlan) -> "SubscriptionPlanRead":
        return cls(
            tier=plan.tier,
            price=plan.price,
            currency=plan.currency,
            features=list(plan.features),
            description=plan.description,
        )


class SubscriptionUpgradeRequest(BaseModel):
    tier: SubscriptionTier = Field(..., description="Desired subscription tier")
    payment_reference: str | None = Field(default=None, max_length=120)
    duration_days: int = Field(default=30, ge=7, le=365)


class SubscriptionStatusRead(BaseModel):
    tier: SubscriptionTier
    expires_at: datetime | None = None
    started_at: datetime | None = None
