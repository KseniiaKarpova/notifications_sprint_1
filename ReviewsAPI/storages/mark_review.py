from models.review import ReviewMark, Document
from storages import BaseStorage
from schemas.review import MarkReviewDto, UpdateMarkReviewDto
from schemas.author import Author
from uuid import UUID
from exceptions import already_exists, deleted
from pymongo.errors import DuplicateKeyError


class ReviewMarkStorage(BaseStorage):
    document: Document = ReviewMark

    async def mark(self, data: MarkReviewDto, author: Author):
        try:
            return await ReviewMark(
                mark=data.mark,
                review_id=data.review_id,
                author=author.model_dump(),
            ).create()
        except DuplicateKeyError:
            raise already_exists

    async def delete(self, review_mark_id: UUID):
        await self.document.find({'_id': review_mark_id}).delete()
        return deleted

    async def update(self, review_mark_id: UUID, data: UpdateMarkReviewDto):
        return await ReviewMark.find_one({'_id': review_mark_id}).update(
            {"$set": data.model_dump(exclude_none=True, exclude_unset=True)})

    async def get(self, **kwargs):
        return await ReviewMark.find_one(kwargs)
