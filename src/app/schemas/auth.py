from datetime import datetime

from pydantic import BaseModel

from app.domain import SubscriptionTier


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    subscription_tier: SubscriptionTier
