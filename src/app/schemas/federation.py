from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.federation import FederationSubmissionStatus
from app.schemas.user import EmailField


class FederationSubmissionBase(BaseModel):
    federation_name: str = Field(..., min_length=3, max_length=120)
    contact_email: EmailField
    payload_url: str = Field(..., description="Public or signed URL where the result file can be fetched")
    notes: str | None = Field(default=None, max_length=500)


class FederationSubmissionCreate(FederationSubmissionBase):
    access_token: str = Field(..., min_length=8, max_length=128)


class FederationSubmissionRead(FederationSubmissionBase):
    id: int
    status: FederationSubmissionStatus
    submitted_at: datetime = Field(alias="created_at")
    processed_at: datetime | None = None
    verified_at: datetime | None = None
    status_details: str | None = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
