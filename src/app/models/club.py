from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .federation import Federation
    from .roster import Roster
    from .user import User


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    federation_id: Mapped[int | None] = mapped_column(
        ForeignKey("federations.id", ondelete="SET NULL"), nullable=True
    )
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    country: Mapped[str] = mapped_column(String(80), nullable=False)

    federation: Mapped["Federation | None"] = relationship(
        "Federation", back_populates="clubs", lazy="joined"
    )
    manager: Mapped["User | None"] = relationship(
        "User", back_populates="managed_clubs", lazy="joined"
    )
    rosters: Mapped[list["Roster"]] = relationship(
        "Roster", back_populates="club", cascade="all, delete-orphan"
    )
