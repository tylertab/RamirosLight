from datetime import datetime

from pydantic import BaseModel, Field


class FederationSubmissionBase(BaseModel):
    federation_name: str = Field(..., min_length=3, max_length=120)
    contact_email: str = Field(..., min_length=5, max_length=120)
    payload_url: str = Field(..., description="Public or signed URL where the result file can be fetched")
    notes: str | None = Field(default=None, max_length=500)


class FederationSubmissionCreate(FederationSubmissionBase):
    pass


class FederationSubmissionRead(FederationSubmissionBase):
    id: int
    status: str
    submitted_at: datetime

    class Config:
        from_attributes = True
