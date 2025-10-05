from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    federation_id: Mapped[int] = mapped_column(ForeignKey("federations.id"), index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    city: Mapped[str | None] = mapped_column(String(80), nullable=True)
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)

    federation: Mapped["Federation"] = relationship("Federation", back_populates="clubs")
    rosters: Mapped[list["Roster"]] = relationship(
        "Roster", back_populates="club", cascade="all, delete-orphan"
    )
