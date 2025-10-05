from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select

from app.core.database import DatabaseSessionManager
from app.core.singleton import SingletonMeta
from app.models import EmailSubscriber
from app.schemas.subscriber import EmailSubscriberCreate, EmailSubscriberRead


class EmailSubscriptionService(metaclass=SingletonMeta):
    """Singleton service that manages email subscriber registrations."""

    def __init__(self) -> None:
        self._sessions = DatabaseSessionManager()

    async def subscribe(self, payload: EmailSubscriberCreate) -> EmailSubscriberRead:
        normalized_email = payload.email.strip().lower()
        session = self._sessions.session()
        try:
            existing = await session.execute(
                select(EmailSubscriber).where(EmailSubscriber.email == normalized_email)
            )
            subscriber = existing.scalar_one_or_none()
            if subscriber is not None:
                return EmailSubscriberRead.model_validate(subscriber)

            subscriber = EmailSubscriber(email=normalized_email, locale=payload.locale)
            session.add(subscriber)
            await session.commit()
            await session.refresh(subscriber)
            return EmailSubscriberRead.model_validate(subscriber)
        except Exception as exc:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to add subscriber",
            ) from exc
        finally:
            await session.close()


def get_email_subscription_service() -> EmailSubscriptionService:
    return EmailSubscriptionService()
