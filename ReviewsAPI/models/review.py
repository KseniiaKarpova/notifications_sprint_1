from uuid import UUID
from schemas.author import Author
from beanie import Document
from pydantic import Field
from models import BaseMixin


class FilmReview(BaseMixin, Document):
    film_id: UUID
    author: Author
    text: str | None = Field(None)
    mark: int = Field(ge=0, le=10)

    class Settings:
        name = "film_review"
        use_state_management = True


class ReviewMark(BaseMixin, Document):
    review_id: UUID
    mark: int = Field(ge=0, le=10)
    author: Author

    class Settings:
        name = "review_mark"
        use_state_management = True
