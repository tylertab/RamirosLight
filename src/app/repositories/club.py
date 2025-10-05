from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Club

from .base import SQLAlchemyRepository


class ClubRepository(SQLAlchemyRepository[Club]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Club)

    async def get_with_rosters(self, club_id: int) -> Club | None:
        stmt = (
            select(Club)
            .options(selectinload(Club.rosters))
            .where(Club.id == club_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_with_associations(self) -> list[Club]:
        stmt = select(Club).options(selectinload(Club.rosters))
        result = await self._session.execute(stmt)
        return result.scalars().all()
