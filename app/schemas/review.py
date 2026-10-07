from datetime import datetime

from pydantic import BaseModel, Field


class ReviewIssueResponse(BaseModel):
    id: int
    severity: str
    category: str
    line: int | None
    message: str
    suggestion: str | None

    class Config:
        from_attributes = True


class CodeReviewRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: str = Field(..., min_length=1, max_length=50)
    mode: str = Field(default="local")


class CodeReviewResponse(BaseModel):
    id: int
    code: str
    language: str
    score: int | None
    summary: str | None
    created_at: datetime | None
    issues: list[ReviewIssueResponse] = []

    class Config:
        from_attributes = True