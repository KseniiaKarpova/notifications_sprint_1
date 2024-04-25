from pymongo.errors import DuplicateKeyError
from models.review import FilmReview, Document, ReviewMark
from storages import BaseStorage
from schemas.review import MarkFilmDto, UpdateMarkFilmDto
from schemas.author import Author
from uuid import UUID
from exceptions import already_exists, deleted


class ReviewFilmStorage(BaseStorage):
    document: Document = FilmReview

    async def mark(self, data: MarkFilmDto, author: Author):
        try:
            return await FilmReview(
                film_id=data.film_id,
                mark=data.mark,
                text=data.text,
                author=author.model_dump(),
            ).create()
        except DuplicateKeyError:
            raise already_exists

    async def delete(self, review_id: UUID):
        await FilmReview.find({'_id': review_id}).delete()
        return deleted

    async def update(self, review_id: UUID, data: UpdateMarkFilmDto):
        return await FilmReview.find_one({'_id': review_id}).update(
            {"$set": data.model_dump(exclude_none=True, exclude_unset=True)})

    async def get(self, **kwargs):
        return await FilmReview.find_one(kwargs)

    async def get_with_marks(self, film_id: UUID):
        return await FilmReview.aggregate(
            [
                {"$match": {"film_id": film_id}},  # Match FilmReview documents by the specific film_id
                {"$lookup": {
                    "from": ReviewMark.get_motor_collection().name,
                    "localField": "_id",
                    "foreignField": "review_id",
                    "as": "review_marks"}}
                    ]).to_list()
