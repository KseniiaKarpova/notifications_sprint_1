from storages.review_film import ReviewFilmStorage
from services import BaseService
from abc import abstractmethod
from schemas.review import MarkFilmDto, UpdateMarkFilmDto
from schemas.author import Author
from schemas.auth import JWTUserData
from fastapi import Depends
from models.review import FilmReview
from uuid import UUID


class BaseReviewFilmService(BaseService):
    def __init__(
            self,
            storage: ReviewFilmStorage,
            dto: MarkFilmDto = None) -> None:
        self.storage = storage
        self.dto = dto

    @abstractmethod
    async def set_like(self):
        pass

    @abstractmethod
    async def set_dislike(self):
        pass

    @abstractmethod
    async def set_review(self):
        pass


class ReviewFilmService(BaseReviewFilmService):
    async def set_like(self, user: JWTUserData) -> FilmReview:
        author = await self.author(data=user)
        return await self.storage.mark(data=self.dto, author=author)

    async def set_dislike(self, user: JWTUserData):
        author = await self.author(data=user)
        return await self.storage.mark(data=self.dto, author=author)

    async def set_review(self, user: JWTUserData):
        author = await self.author(data=user)
        return await self.storage.mark(data=self.dto, author=author)

    async def update_get(self, review_id: UUID, data: UpdateMarkFilmDto):
        await self.storage.update(review_id=review_id, data=data)
        return await self.storage.get(_id=review_id)

    async def delete_review(self, review_id: UUID):
        return await self.storage.delete(review_id=review_id)

    async def author(self, data: JWTUserData):
        return Author(id=data.uuid, first_name=data.name, last_name=data.surname)

    async def get_film_reviews(self, film_id: UUID):
        return await self.storage.get_with_marks(film_id=film_id)


def get_film_review_service(
        storage: ReviewFilmStorage = Depends(ReviewFilmStorage),
        ) -> ReviewFilmService:
    return ReviewFilmService(storage=storage)
