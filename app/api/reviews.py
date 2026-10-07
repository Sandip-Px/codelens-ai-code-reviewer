from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.code_review import CodeReview
from app.models.review_issue import ReviewIssue
from app.schemas.review import (
    CodeReviewRequest,
    CodeReviewResponse
)
from app.services.analyzer import CodeAnalyzer

from app.services.ai_analyzer import AIAnalyzer

router = APIRouter(
    prefix="/api/reviews",
    tags=["Code Reviews"]
)

local_analyzer = CodeAnalyzer()

def get_analyzer(mode: str):
    mode = mode.lower()

    if mode == "ai":
        return AIAnalyzer()

    return local_analyzer

@router.post("/", response_model=CodeReviewResponse)
def create_review(
    request: CodeReviewRequest,
    db: Session = Depends(get_db)
):
    analyzer = get_analyzer(request.mode)

    analysis = analyzer.analyze(
        request.code,
        request.language
    )

    review = CodeReview(
        code=request.code,
        language=request.language,
        score=analysis["score"],
        summary=analysis["summary"]
    )

    db.add(review)
    db.flush()

    for issue in analysis["issues"]:
        db_issue = ReviewIssue(
            review_id=review.id,
            severity=issue["severity"],
            category=issue["category"],
            line=issue["line"],
            message=issue["message"],
            suggestion=issue["suggestion"]
        )

        db.add(db_issue)

    db.commit()
    db.refresh(review)

    return review


@router.get("/", response_model=list[CodeReviewResponse])
def get_reviews(
    db: Session = Depends(get_db)
):
    return (
        db.query(CodeReview)
        .order_by(CodeReview.created_at.desc())
        .limit(20)
        .all()
    )


@router.get("/{review_id}", response_model=CodeReviewResponse)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(CodeReview)
        .filter(CodeReview.id == review_id)
        .first()
    )