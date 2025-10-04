from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Roster
from app.schemas.roster import RosterCreate, RosterRead


class RostersService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_roster(self, payload: RosterCreate, owner_id: int | None) -> RosterRead:
        roster = Roster(
            **payload.model_dump(exclude_none=True),
            updated_at=datetime.now(tz=timezone.utc),
            owner_id=owner_id,
        )
        self._session.add(roster)
        await self._session.commit()
        await self._session.refresh(roster)
        return RosterRead.model_validate(roster)

    async def list_rosters(self) -> list[RosterRead]:
        result = await self._session.execute(select(Roster).order_by(Roster.updated_at.desc()))
        rosters = result.scalars().all()
        return [RosterRead.model_validate(item) for item in rosters]


async def get_rosters_service(session: AsyncSession = Depends(get_session)) -> RostersService:
    return RostersService(session)
