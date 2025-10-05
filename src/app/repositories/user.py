from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AthleteProfile, Roster, User

from .base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_by(User.email, email)


class AthleteProfileRepository(SQLAlchemyRepository[AthleteProfile]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AthleteProfile)

    async def get_by_user_id(self, user_id: int) -> AthleteProfile | None:
        return await self.get_by(AthleteProfile.user_id, user_id)

    async def list_for_roster_owner(self, roster_owner_id: int) -> list[AthleteProfile]:
        stmt = (
            select(AthleteProfile)
            .join(User, User.id == AthleteProfile.user_id)
            .where(User.id == roster_owner_id)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()


class RosterRepository(SQLAlchemyRepository[Roster]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Roster)

    async def list_recent(self) -> list[Roster]:
        stmt = select(Roster).order_by(Roster.updated_at.desc())
        result = await self._session.execute(stmt)
        return result.scalars().all()
