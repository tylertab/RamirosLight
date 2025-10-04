from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import PasswordHasher
from app.models import User
from app.schemas.user import UserCreate, UserRead


class AccountsService:
    def __init__(self, session: AsyncSession, password_hasher: PasswordHasher | None = None) -> None:
        self._session = session
        self._hasher = password_hasher or PasswordHasher()

    async def get_user_by_email(self, email: str) -> UserRead | None:
        result = await self._session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return UserRead.model_validate(user) if user else None

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        result = await self._session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return UserRead.model_validate(user) if user else None

    async def create_user(self, payload: UserCreate) -> UserRead:
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            role=payload.role,
            hashed_password=self._hasher.hash(payload.password),
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return UserRead.model_validate(user)

    async def list_users(self) -> list[UserRead]:
        result = await self._session.execute(select(User))
        users = result.scalars().all()
        return [UserRead.model_validate(user) for user in users]


async def get_accounts_service(
    session: AsyncSession = Depends(get_session),
) -> AccountsService:
    return AccountsService(session)
