from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import PasswordHasher
from app.models import AthleteProfile, User
from app.repositories.user import AthleteProfileRepository, UserRepository
from app.schemas.user import UserCreate, UserRead


class AccountsService:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher | None = None,
        user_repository: UserRepository | None = None,
        athlete_repository: AthleteProfileRepository | None = None,
    ) -> None:
        self._session = session
        self._hasher = password_hasher or PasswordHasher()
        self._users = user_repository or UserRepository(session)
        self._athletes = athlete_repository or AthleteProfileRepository(session)

    async def get_user_by_email(self, email: str) -> UserRead | None:
        user = await self._users.get_by_email(email)
        return UserRead.model_validate(user) if user else None

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        user = await self._users.get(user_id)
        return UserRead.model_validate(user) if user else None

    async def create_user(self, payload: UserCreate) -> UserRead:
        started_at = datetime.now(tz=timezone.utc)
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            role=payload.role,
            hashed_password=self._hasher.hash(payload.password),
        )
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

    async def get_user_model(self, user_id: int) -> User | None:
        return await self._users.get(user_id)


async def get_accounts_service(
    session: AsyncSession = Depends(get_session),
) -> AccountsService:
    return AccountsService(session)
