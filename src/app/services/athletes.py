from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import AthleteProfile
from app.schemas.athlete import (
    AthleteHistoryEntry,
    AthleteHistoryResponse,
    AthleteProfileRead,
    AthleteProfileUpdate,
)


class AthletesService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

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
        result = await self._session.execute(select(AthleteProfile).where(AthleteProfile.user_id == user_id))
        profile = result.scalar_one_or_none()
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
