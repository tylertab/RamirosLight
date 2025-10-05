from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Club, Roster
from app.repositories.club import ClubRepository
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
        club_repository: ClubRepository | None = None,
    ) -> None:
        self._session = session
        self._rosters = roster_repository or RosterRepository(session)
        self._users = user_repository or UserRepository(session)
        self._athletes = athlete_repository or AthleteProfileRepository(session)
        self._clubs = club_repository or ClubRepository(session)

    async def create_roster(self, payload: RosterCreate, owner_id: int | None) -> RosterRead:
        club = None
        if payload.club_id is not None:
            club = await self._clubs.get(payload.club_id)
            if club is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")
            if club.manager_id is None and owner_id is not None:
                club.manager_id = owner_id
                await self._session.flush()
        elif payload.club is not None:
            existing = await self._clubs.get_by(Club.name, payload.club.name)
            if existing is None:
                club = Club(
                    name=payload.club.name,
                    city=payload.club.city,
                    country=payload.club.country,
                    federation_id=payload.club.federation_id,
                    manager_id=owner_id,
                )
                await self._clubs.add(club)
            else:
                club = existing
                if club.manager_id is None and owner_id is not None:
                    club.manager_id = owner_id
                    await self._session.flush()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Club information required")

        roster_data = payload.model_dump(exclude_none=True, exclude={"club"})
        roster = Roster(
            **{key: value for key, value in roster_data.items() if key not in {"club_id"}},
            updated_at=datetime.now(tz=timezone.utc),
            club_id=club.id if club else payload.club_id,
        )
        await self._rosters.add(roster)
        await self._session.commit()
        roster = await self._rosters.get_with_associations(roster.id)
        if roster is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Roster creation failed")
        return RosterRead.model_validate(roster)

    async def list_rosters(self) -> list[RosterRead]:
        rosters = await self._rosters.list_recent()
        return [RosterRead.model_validate(item) for item in rosters]

    async def get_roster(self, roster_id: int) -> RosterDetail:
        roster = await self._rosters.get_with_associations(roster_id)
        if roster is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roster not found")
        owner = None
        if roster.club and roster.club.manager is not None:
            owner = UserRead.model_validate(roster.club.manager)
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
        roster_payload = RosterRead.model_validate(roster)
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
            club=roster_payload.club,
            federation=roster_payload.federation,
        )


async def get_rosters_service(session: AsyncSession = Depends(get_session)) -> RostersService:
    return RostersService(session)
