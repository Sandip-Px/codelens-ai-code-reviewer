from app.database.database import Base, engine

from app.models.code_review import CodeReview
from app.models.review_issue import ReviewIssue


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()