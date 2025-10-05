from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, String
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:  # pragma: no cover
    from .club import Club


class Federation(Base):
    __tablename__ = "federations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)

    clubs: Mapped[list["Club"]] = relationship(
        "Club", back_populates="federation", cascade="all, delete-orphan"
    )


class FederationSubmissionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class FederationSubmission(Base):
    __tablename__ = "federation_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    federation_name: Mapped[str] = mapped_column(String(120), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)
    payload_url: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[FederationSubmissionStatus] = mapped_column(
        SqlEnum(FederationSubmissionStatus, native_enum=False, length=20),
        nullable=False,
        default=FederationSubmissionStatus.QUEUED,
    )
    status_details: Mapped[str | None] = mapped_column(String(500), nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
