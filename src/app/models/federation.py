from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class FederationSubmission(Base):
    __tablename__ = "federation_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    federation_name: Mapped[str] = mapped_column(String(120), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(255), nullable=False)
    payload_url: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
