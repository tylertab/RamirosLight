from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Roster
from app.repositories.user import AthleteProfileRepository, RosterRepository, UserRepository
from app.schemas.athlete import AthleteSummary
from app.schemas.roster import RosterCreate, RosterDetail, RosterRead
from app.schemas.user import UserRead


class RostersService:
    def __init__(
        self,
        session: AsyncSession,
        roster_repository: RosterRepository | None = None,
        user_repository: UserRepository | None = None,
        athlete_repository: AthleteProfileRepository | None = None,
    ) -> None:
        self._session = session
        self._rosters = roster_repository or RosterRepository(session)
        self._users = user_repository or UserRepository(session)
        self._athletes = athlete_repository or AthleteProfileRepository(session)

    async def create_roster(self, payload: RosterCreate, owner_id: int | None) -> RosterRead:
        roster = Roster(
            **payload.model_dump(exclude_none=True),
            updated_at=datetime.now(tz=timezone.utc),
            owner_id=owner_id,
        )
        await self._rosters.add(roster)
        await self._session.commit()
        await self._session.refresh(roster)
        return RosterRead.model_validate(roster)

    async def list_rosters(self) -> list[RosterRead]:
        rosters = await self._rosters.list_recent()
        return [RosterRead.model_validate(item) for item in rosters]

    async def get_roster(self, roster_id: int) -> RosterDetail:
        roster = await self._rosters.get(roster_id)
        if roster is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roster not found")
        owner = None
        if roster.owner_id is not None:
            user = await self._users.get(roster.owner_id)
            if user is not None:
                owner = UserRead.model_validate(user)
        athletes: list[AthleteSummary] = []
        if owner:
            profiles = await self._athletes.list_for_roster_owner(owner.id)
            for profile in profiles:
                user = await self._users.get(profile.user_id)
                if user is None:
                    continue
                athletes.append(
                    AthleteSummary(
                        id=user.id,
                        full_name=user.full_name,
                        email=user.email,
                        bio=profile.bio,
                    )
                )
        return RosterDetail(
            id=roster.id,
            name=roster.name,
            country=roster.country,
            division=roster.division,
            coach_name=roster.coach_name,
            athlete_count=roster.athlete_count,
            updated_at=roster.updated_at,
            owner=owner,
            athletes=athletes,
        )


async def get_rosters_service(session: AsyncSession = Depends(get_session)) -> RostersService:
    return RostersService(session)
