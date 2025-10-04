from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import AthleteProfile
from app.repositories.user import (
    AthleteProfileRepository,
    RosterRepository,
    UserRepository,
)
from app.schemas.athlete import (
    AthleteDetail,
    AthleteHistoryEntry,
    AthleteHistoryResponse,
    AthleteProfileRead,
    AthleteProfileUpdate,
    AthleteRosterSummary,
)


class AthletesService:
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository | None = None,
        athlete_repository: AthleteProfileRepository | None = None,
        roster_repository: RosterRepository | None = None,
    ) -> None:
        self._session = session
        self._users = user_repository or UserRepository(session)
        self._athletes = athlete_repository or AthleteProfileRepository(session)
        self._rosters = roster_repository or RosterRepository(session)

    async def get_detail(self, user_id: int) -> AthleteDetail:
        user = await self._users.get(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")
        profile = await self._fetch_profile(user_id)
        rosters = await self._rosters.list_owned_by(user_id)
        roster_payload = [AthleteRosterSummary.model_validate(item) for item in rosters]
        entries = [AthleteHistoryEntry(**entry) for entry in profile.track_history]
        return AthleteDetail(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            role=user.role,
            subscription_tier=user.subscription_tier.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
            bio=profile.bio,
            track_history=entries,
            highlight_video_url=profile.highlight_video_url,
            rosters=roster_payload,
        )

    async def get_profile(self, user_id: int) -> AthleteProfileRead:
        profile = await self._fetch_profile(user_id)
        return self._to_read_model(profile)

    async def get_history(self, user_id: int) -> AthleteHistoryResponse:
        profile = await self._fetch_profile(user_id)
        entries = [AthleteHistoryEntry(**entry) for entry in profile.track_history]
        return AthleteHistoryResponse(athlete_id=user_id, history=entries)

    async def update_profile(self, user_id: int, payload: AthleteProfileUpdate) -> AthleteProfileRead:
        profile = await self._fetch_profile(user_id)
        if payload.bio is not None:
            profile.bio = payload.bio
        if payload.track_history is not None:
            profile.track_history = [entry.model_dump() for entry in payload.track_history]
        if payload.highlight_video_url is not None:
            profile.highlight_video_url = payload.highlight_video_url
        self._session.add(profile)
        await self._session.commit()
        await self._session.refresh(profile)
        return self._to_read_model(profile)

    async def _fetch_profile(self, user_id: int) -> AthleteProfile:
        profile = await self._athletes.get_by_user_id(user_id)
        if profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete profile not found")
        return profile

    def _to_read_model(self, profile: AthleteProfile) -> AthleteProfileRead:
        entries = [AthleteHistoryEntry(**entry) for entry in profile.track_history]
        return AthleteProfileRead(
            user_id=profile.user_id,
            bio=profile.bio,
            track_history=entries,
            highlight_video_url=profile.highlight_video_url,
        )


async def get_athletes_service(session: AsyncSession = Depends(get_session)) -> AthletesService:
    return AthletesService(session)
