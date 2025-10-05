from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class EmailSubscriber(Base):
    __tablename__ = "email_subscribers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    locale: Mapped[str | None] = mapped_column(String(10), nullable=True)
