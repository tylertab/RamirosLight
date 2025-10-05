from datetime import datetime, timezone
from hashlib import sha256
from urllib.parse import urlparse

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DatabaseSessionManager, get_session
from app.integrations.message_bus import MessageBus
from app.models import Federation, FederationSubmission, FederationSubmissionStatus
from app.schemas.federation import FederationSubmissionCreate, FederationSubmissionRead


class FederationIngestionService:
    def __init__(self, session: AsyncSession, message_bus: MessageBus | None = None) -> None:
        self._session = session
        self._message_bus = message_bus or MessageBus()

    async def enqueue_submission(
        self, payload: FederationSubmissionCreate
    ) -> FederationSubmissionRead:
        federation = await self._validate_payload(payload)
        submission = FederationSubmission(
            **payload.model_dump(exclude={"access_token"}),
            status=FederationSubmissionStatus.QUEUED,
        )
        self._session.add(submission)
        await self._session.commit()
        await self._session.refresh(submission)

        await self._message_bus.publish("federation.submission", submission.id)
        return FederationSubmissionRead.model_validate(submission)

    async def list_submissions(self) -> list[FederationSubmissionRead]:
        result = await self._session.execute(select(FederationSubmission))
        submissions = result.scalars().all()
        return [FederationSubmissionRead.model_validate(item) for item in submissions]

    async def _validate_payload(self, payload: FederationSubmissionCreate) -> Federation:
        parsed = urlparse(payload.payload_url)
        if parsed.scheme not in {"https", "s3"}:
            raise ValueError("Payload URL must be HTTPS or signed storage URL")
        if not parsed.netloc:
            raise ValueError("Payload URL must include a host")
        token = payload.access_token.strip()
        if not token:
            raise ValueError("Federation access token is required")

        result = await self._session.execute(
            select(Federation).where(Federation.name == payload.federation_name)
        )
        federation = result.scalar_one_or_none()
        if federation is None or not federation.ingest_token_hash:
            raise ValueError("Federation not registered for secure uploads")

        provided_hash = sha256(token.encode("utf-8")).hexdigest()
        if provided_hash != federation.ingest_token_hash:
            raise ValueError("Invalid federation access token")

        return federation


async def get_federation_service(
    session: AsyncSession = Depends(get_session),
) -> FederationIngestionService:
    return FederationIngestionService(session)


class FederationSubmissionProcessor:
    def __init__(self, message_bus: MessageBus | None = None) -> None:
        self._bus = message_bus or MessageBus()
        self._bus.subscribe("federation.submission", self._handle)

    async def _handle(self, submission_id: int) -> None:
        session = DatabaseSessionManager().session()
        try:
            submission = await session.get(FederationSubmission, submission_id)
            if submission is None:
                return
            submission.status = FederationSubmissionStatus.PROCESSING
            submission.processed_at = datetime.now(tz=timezone.utc)
            session.add(submission)
            await session.commit()

            checksum = sha256(submission.payload_url.encode("utf-8")).hexdigest()
            submission.checksum = checksum
            submission.verified_at = datetime.now(tz=timezone.utc)
            submission.status = FederationSubmissionStatus.PROCESSED
            submission.status_details = "Validated payload URL and queued ingestion."
            session.add(submission)
            await session.commit()
        except Exception as exc:  # pragma: no cover - defensive fallback
            if "submission" in locals() and submission is not None:
                submission.status = FederationSubmissionStatus.FAILED
                submission.status_details = str(exc)
                session.add(submission)
                await session.commit()
        finally:
            await session.close()


_processor = FederationSubmissionProcessor()

