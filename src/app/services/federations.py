from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.integrations.message_bus import MessageBus
from app.models import FederationSubmission
from app.schemas.federation import FederationSubmissionCreate, FederationSubmissionRead


class FederationIngestionService:
    def __init__(self, session: AsyncSession, message_bus: MessageBus | None = None) -> None:
        self._session = session
        self._message_bus = message_bus or MessageBus()

    async def enqueue_submission(
        self, payload: FederationSubmissionCreate
    ) -> FederationSubmissionRead:
        submission = FederationSubmission(**payload.model_dump(), status="queued")
        self._session.add(submission)
        await self._session.commit()
        await self._session.refresh(submission)

        await self._message_bus.publish("federation.submission", submission.id)
        return FederationSubmissionRead.model_validate(submission)

    async def list_submissions(self) -> list[FederationSubmissionRead]:
        result = await self._session.execute(select(FederationSubmission))
        submissions = result.scalars().all()
        return [FederationSubmissionRead.model_validate(item) for item in submissions]


async def get_federation_service(
    session: AsyncSession = Depends(get_session),
) -> FederationIngestionService:
    return FederationIngestionService(session)
