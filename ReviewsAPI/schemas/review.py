from pydantic import BaseModel
from uuid import UUID
from pydantic import Field


class MarkFilmDto(BaseModel):
    film_id: UUID
    mark: int = Field(ge=0, le=10)
    text: str | None = Field(None)


class UpdateMarkFilmDto(BaseModel):
    mark: int = Field(ge=0, le=10)
    text: str | None = Field(None)


class LikeDislikeFilmDto(BaseModel):
    film_id: UUID


class DeleteMarkFilmDto(BaseModel):
    review_id: UUID


class MarkReviewDto(BaseModel):
    review_id: UUID
    mark: int = Field(ge=0, le=10)


class UpdateMarkReviewDto(BaseModel):
    mark: int = Field(ge=0, le=10)
