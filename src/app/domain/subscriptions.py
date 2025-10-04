from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Sequence


class SubscriptionTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    COACH = "coach"

    @property
    def order(self) -> int:
        order_map = {
            SubscriptionTier.FREE: 0,
            SubscriptionTier.PREMIUM: 1,
            SubscriptionTier.COACH: 2,
        }
        return order_map[self]

    def meets(self, minimum: "SubscriptionTier") -> bool:
        return self.order >= minimum.order


class SubscriptionFeature(str, Enum):
    GLOBAL_SEARCH = "global_search"
    ATHLETE_HISTORY = "athlete_history"
    RACE_VIDEOS = "race_videos"
    ROSTER_MANAGEMENT = "roster_management"
    FEDERATION_UPLOAD = "federation_upload"


@dataclass(frozen=True)
class SubscriptionPlan:
    tier: SubscriptionTier
    price: float
    currency: str
    features: Sequence[SubscriptionFeature]
    description: str


class SubscriptionStrategy(Protocol):
    """Strategy contract for subscription entitlement calculations."""

    def plan(self) -> SubscriptionPlan:
        ...

    def allows(self, feature: SubscriptionFeature) -> bool:
        ...


class BaseSubscriptionStrategy:
    def __init__(self, plan: SubscriptionPlan) -> None:
        self._plan = plan

    def plan(self) -> SubscriptionPlan:
        return self._plan

    def allows(self, feature: SubscriptionFeature) -> bool:
        return feature in self._plan.features


class FreePlanStrategy(BaseSubscriptionStrategy):
    pass


class PremiumPlanStrategy(BaseSubscriptionStrategy):
    pass


class CoachPlanStrategy(BaseSubscriptionStrategy):
    pass
