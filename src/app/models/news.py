from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class NewsAudience(str, Enum):
    PUBLIC = "public"
    PREMIUM = "premium"
    COACH = "coach"


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    region: Mapped[str] = mapped_column(String(120), nullable=True)
    excerpt: Mapped[str] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    audience: Mapped[NewsAudience] = mapped_column(
        SqlEnum(NewsAudience, native_enum=False, length=20),
        nullable=False,
        default=NewsAudience.PUBLIC,
    )
