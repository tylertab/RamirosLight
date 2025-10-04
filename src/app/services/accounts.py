from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import PasswordHasher
from app.domain import SubscriptionTier
from app.models import AthleteProfile, User
from app.schemas.user import UserCreate, UserRead
from app.services.subscriptions import SubscriptionService, get_subscription_service


class AccountsService:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher | None = None,
        subscription_service: SubscriptionService | None = None,
    ) -> None:
        self._session = session
        self._hasher = password_hasher or PasswordHasher()
        self._subscriptions = subscription_service or SubscriptionService()

    async def get_user_by_email(self, email: str) -> UserRead | None:
        user = await self._get_user_model_by_email(email)
        return UserRead.model_validate(user) if user else None

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        user = await self._get_user_model_by_id(user_id)
        return UserRead.model_validate(user) if user else None

    async def create_user(self, payload: UserCreate) -> UserRead:
        tier = SubscriptionTier(payload.subscription_tier)
        started_at = datetime.now(tz=timezone.utc)
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            role=payload.role,
            hashed_password=self._hasher.hash(payload.password),
            subscription_tier=tier,
        )
        user.activate_subscription(tier, duration_days=30, reference="signup", started_at=started_at)
        self._session.add(user)
        await self._session.flush()

        if payload.role.lower() == "athlete":
            default_history = [
                {
                    "event": "Trackeo Trials 400m",
                    "event_date": started_at.date().isoformat(),
                    "result": "52.10s",
                    "video_url": None,
                }
            ]
            profile = AthleteProfile(user_id=user.id, track_history=default_history)
            self._session.add(profile)

        await self._session.commit()
        await self._session.refresh(user)
        return UserRead.model_validate(user)

    async def list_users(self) -> list[UserRead]:
        result = await self._session.execute(select(User))
        users = result.scalars().all()
        return [UserRead.model_validate(user) for user in users]

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self._get_user_model_by_email(email)
        if user and self._hasher.verify(password, user.hashed_password):
            return user
        return None

    async def upgrade_subscription(
        self,
        user: User,
        tier: SubscriptionTier,
        duration_days: int,
        payment_reference: str | None,
    ) -> User:
        now = datetime.now(tz=timezone.utc)
        self._subscriptions.apply_upgrade(user, tier, duration_days, payment_reference, now)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_user_model(self, user_id: int) -> User | None:
        return await self._get_user_model_by_id(user_id)

    async def _get_user_model_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def _get_user_model_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


async def get_accounts_service(
    session: AsyncSession = Depends(get_session),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
) -> AccountsService:
    return AccountsService(session, subscription_service=subscription_service)
