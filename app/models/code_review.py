from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(Text, nullable=False)

    language = Column(String(50), nullable=False)

    score = Column(Integer, nullable=True)

    summary = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    issues = relationship(
        "ReviewIssue",
        back_populates="review",
        cascade="all, delete-orphan"
    )