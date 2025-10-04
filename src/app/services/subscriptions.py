from __future__ import annotations

from datetime import datetime

from app.core.config import SettingsSingleton
from app.core.singleton import SingletonMeta
from app.domain import (
    CoachPlanStrategy,
    FreePlanStrategy,
    PremiumPlanStrategy,
    SubscriptionFeature,
    SubscriptionPlan,
    SubscriptionStrategy,
    SubscriptionTier,
)
from app.models import User
from app.schemas.user import UserRead


class SubscriptionService(metaclass=SingletonMeta):
    def __init__(self) -> None:
        settings = SettingsSingleton().instance
        currency = settings.subscription_currency
        pricing = settings.subscription_pricing
        self._strategies: dict[SubscriptionTier, SubscriptionStrategy] = {
            SubscriptionTier.FREE: FreePlanStrategy(
                SubscriptionPlan(
                    tier=SubscriptionTier.FREE,
                    price=pricing.get(SubscriptionTier.FREE.value, 0.0),
                    currency=currency,
                    features=(SubscriptionFeature.GLOBAL_SEARCH,),
                    description="Discover athletes, events, and headlines with limited detail.",
                )
            ),
            SubscriptionTier.PREMIUM: PremiumPlanStrategy(
                SubscriptionPlan(
                    tier=SubscriptionTier.PREMIUM,
                    price=pricing.get(SubscriptionTier.PREMIUM.value, 12.0),
                    currency=currency,
                    features=(
                        SubscriptionFeature.GLOBAL_SEARCH,
                        SubscriptionFeature.ATHLETE_HISTORY,
                        SubscriptionFeature.RACE_VIDEOS,
                    ),
                    description="Unlock complete athlete histories and on-demand race videos.",
                )
            ),
            SubscriptionTier.COACH: CoachPlanStrategy(
                SubscriptionPlan(
                    tier=SubscriptionTier.COACH,
                    price=pricing.get(SubscriptionTier.COACH.value, 29.0),
                    currency=currency,
                    features=(
                        SubscriptionFeature.GLOBAL_SEARCH,
                        SubscriptionFeature.ATHLETE_HISTORY,
                        SubscriptionFeature.RACE_VIDEOS,
                        SubscriptionFeature.ROSTER_MANAGEMENT,
                        SubscriptionFeature.FEDERATION_UPLOAD,
                    ),
                    description="Designed for staffs and federations managing teams across regions.",
                )
            ),
        }

    def plans(self) -> list[SubscriptionPlan]:
        return [strategy.plan() for strategy in self._strategies.values()]

    def plan_for(self, tier: SubscriptionTier) -> SubscriptionPlan:
        return self._strategies[tier].plan()

    def allows(self, tier: SubscriptionTier, feature: SubscriptionFeature) -> bool:
        strategy = self._strategies[tier]
        return strategy.allows(feature)

    def user_has_feature(self, user: User | UserRead, feature: SubscriptionFeature) -> bool:
        tier_value = user.subscription_tier if isinstance(user, User) else user.subscription_tier
        tier = SubscriptionTier(tier_value)
        return self.allows(tier, feature)

    def apply_upgrade(
        self,
        user: User,
        tier: SubscriptionTier,
        duration_days: int,
        payment_reference: str | None,
        started_at: datetime,
    ) -> None:
        user.activate_subscription(tier, duration_days, payment_reference, started_at)


def get_subscription_service() -> SubscriptionService:
    return SubscriptionService()
