from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Club, Federation, Roster
from app.repositories.user import RosterRepository
from app.schemas.roster import RosterCreate, RosterDetail, RosterRead


class RostersService:
    def __init__(self, session: AsyncSession, roster_repository: RosterRepository | None = None) -> None:
        self._session = session
        self._rosters = roster_repository or RosterRepository(session)

    async def create_roster(self, payload: RosterCreate) -> RosterRead:
        club = await self._session.get(Club, payload.club_id)
        if club is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

        roster = Roster(
            name=payload.name,
            country=payload.country,
            division=payload.division,
            coach_name=payload.coach_name,
            athlete_count=payload.athlete_count,
            club_id=club.id,
            updated_at=datetime.now(tz=timezone.utc),
        )
        await self._rosters.add(roster)
        await self._session.commit()
        await self._session.refresh(roster)
        return RosterRead(
            id=roster.id,
            name=roster.name,
            country=roster.country,
            division=roster.division,
            coach_name=roster.coach_name,
            athlete_count=roster.athlete_count,
            updated_at=roster.updated_at,
            club_id=club.id,
            club_name=club.name,
        )

    async def list_rosters(self) -> list[RosterRead]:
        stmt = (
            select(Roster, Club)
            .join(Club, Roster.club_id == Club.id)
            .order_by(Roster.updated_at.desc())
        )
        result = await self._session.execute(stmt)
        rows = result.all()
        return [
            RosterRead(
                id=roster.id,
                name=roster.name,
                country=roster.country,
                division=roster.division,
                coach_name=roster.coach_name,
                athlete_count=roster.athlete_count,
                updated_at=roster.updated_at,
                club_id=club.id,
                club_name=club.name,
            )
            for roster, club in rows
        ]

    async def get_roster(self, roster_id: int) -> RosterDetail:
        stmt = (
            select(Roster, Club, Federation)
            .join(Club, Roster.club_id == Club.id)
            .join(Federation, Club.federation_id == Federation.id)
            .where(Roster.id == roster_id)
        )
        result = await self._session.execute(stmt)
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roster not found")
        roster, club, federation = row
        return RosterDetail(
            id=roster.id,
            name=roster.name,
            country=roster.country,
            division=roster.division,
            coach_name=roster.coach_name,
            athlete_count=roster.athlete_count,
            updated_at=roster.updated_at,
            club_id=club.id,
            club_name=club.name,
            club_city=club.city,
            federation_id=federation.id,
            federation_name=federation.name,
        )


async def get_rosters_service(session: AsyncSession = Depends(get_session)) -> RostersService:
    return RostersService(session)
