from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Roster(Base):
    __tablename__ = "rosters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    country: Mapped[str] = mapped_column(String(80), nullable=False)
    division: Mapped[str] = mapped_column(String(80), nullable=False)
    coach_name: Mapped[str] = mapped_column(String(120), nullable=False)
    athlete_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"), nullable=False, index=True)

    club: Mapped["Club"] = relationship("Club", back_populates="rosters")
