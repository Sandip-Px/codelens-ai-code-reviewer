from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class ReviewIssue(Base):
    __tablename__ = "review_issues"

    id = Column(Integer, primary_key=True, index=True)

    review_id = Column(
        Integer,
        ForeignKey("code_reviews.id"),
        nullable=False
    )

    severity = Column(String(20), nullable=False)

    category = Column(String(50), nullable=False)

    line = Column(Integer, nullable=True)

    message = Column(Text, nullable=False)

    suggestion = Column(Text, nullable=True)

    review = relationship(
        "CodeReview",
        back_populates="issues"
    )