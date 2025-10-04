from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain import SubscriptionTier

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(
        Enum(SubscriptionTier, native_enum=False, length=20),
        nullable=False,
        default=SubscriptionTier.FREE,
    )
    subscription_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    subscription_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    subscription_renewal_period_days: Mapped[int] = mapped_column(nullable=False, default=30)
    last_payment_reference: Mapped[str | None] = mapped_column(String(120), nullable=True)

    athlete_profile: Mapped[Optional["AthleteProfile"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )

    def activate_subscription(
        self,
        tier: SubscriptionTier,
        duration_days: int,
        reference: str | None,
        started_at: datetime,
    ) -> None:
        self.subscription_tier = tier
        self.subscription_started_at = started_at
        self.subscription_expires_at = started_at + timedelta(days=duration_days)
        self.subscription_renewal_period_days = duration_days
        self.last_payment_reference = reference


class AthleteProfile(Base):
    __tablename__ = "athlete_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)
    track_history: Mapped[list[dict[str, str]]] = mapped_column(
        JSON, nullable=False, default=list
    )
    highlight_video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user: Mapped[User] = relationship(back_populates="athlete_profile")
