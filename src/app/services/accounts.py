from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import PasswordHasher
from app.domain import SubscriptionTier
from app.models import AthleteProfile, User
from app.repositories.user import (
    AthleteProfileRepository,
    RosterRepository,
    UserRepository,
)
from app.schemas.roster import RosterRead
from app.schemas.user import UserCreate, UserRead
from app.services.subscriptions import SubscriptionService, get_subscription_service


class AccountsService:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher | None = None,
        subscription_service: SubscriptionService | None = None,
        user_repository: UserRepository | None = None,
        athlete_repository: AthleteProfileRepository | None = None,
        roster_repository: RosterRepository | None = None,
    ) -> None:
        self._session = session
        self._hasher = password_hasher or PasswordHasher()
        self._subscriptions = subscription_service or SubscriptionService()
        self._users = user_repository or UserRepository(session)
        self._athletes = athlete_repository or AthleteProfileRepository(session)
        self._rosters = roster_repository or RosterRepository(session)

    async def get_user_by_email(self, email: str) -> UserRead | None:
        user = await self._users.get_by_email(email)
        return UserRead.model_validate(user) if user else None

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        user = await self._users.get(user_id)
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
        await self._users.add(user)

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
            await self._athletes.add(profile)

        await self._session.commit()
        await self._session.refresh(user)
        return UserRead.model_validate(user)

    async def list_users(self) -> list[UserRead]:
        users = await self._users.list()
        return [UserRead.model_validate(user) for user in users]

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self._users.get_by_email(email)
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
        return await self._users.get(user_id)

    async def list_rosters_for_user(self, user_id: int) -> list[RosterRead]:
        rosters = await self._rosters.list_owned_by(user_id)
        return [RosterRead.model_validate(roster) for roster in rosters]


async def get_accounts_service(
    session: AsyncSession = Depends(get_session),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
) -> AccountsService:
    return AccountsService(session, subscription_service=subscription_service)
