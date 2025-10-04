from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    category: str = Field(..., description="Category where the record was found")
    title: str
    subtitle: str | None = None
    detail: str | None = None


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult] = Field(default_factory=list)
