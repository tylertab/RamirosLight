from datetime import datetime

from pydantic import BaseModel, Field

from app.models.news import NewsAudience


class NewsBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    region: str | None = Field(default=None, max_length=120)
    excerpt: str | None = Field(default=None, max_length=500)
    content: str = Field(..., min_length=20)
    audience: NewsAudience = NewsAudience.PUBLIC


class NewsCreate(NewsBase):
    published_at: datetime | None = None


class NewsRead(NewsBase):
    id: int
    published_at: datetime

    class Config:
        from_attributes = True
