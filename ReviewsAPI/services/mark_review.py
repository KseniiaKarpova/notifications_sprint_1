from storages.mark_review import ReviewMarkStorage
from services import BaseService
from schemas.review import MarkReviewDto, UpdateMarkReviewDto
from schemas.author import Author
from schemas.auth import JWTUserData
from fastapi import Depends
from uuid import UUID


class MarkReviewBaseService(BaseService):
    def __init__(
            self,
            storage: ReviewMarkStorage,
            dto: MarkReviewDto = None) -> None:
        self.storage = storage
        self.dto = dto


class MarkReviewService(MarkReviewBaseService):
    async def create_review_mark(self, user: JWTUserData):
        author = await self.author(data=user)
        return await self.storage.mark(data=self.dto, author=author)

    async def delete_review_mark(self, review_mark_id: UUID):
        return await self.storage.delete(review_mark_id=review_mark_id)

    async def author(self, data: JWTUserData):
        return Author(id=data.uuid, first_name=data.name, last_name=data.surname)

    async def update_get(self, review_mark_id: UUID, data: UpdateMarkReviewDto):
        await self.storage.update(review_mark_id=review_mark_id, data=data)
        return await self.storage.get(_id=review_mark_id)


def get_mark_review_service(
        storage: ReviewMarkStorage = Depends(ReviewMarkStorage),
        ) -> MarkReviewService:
    return MarkReviewService(storage=storage)
