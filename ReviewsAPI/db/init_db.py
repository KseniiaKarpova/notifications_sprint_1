from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from models.review import FilmReview, ReviewMark


async def init(*, client: AsyncIOMotorClient) -> None:
    await init_beanie(
        database=getattr(client, settings.mongodb.db_name),
        document_models=[FilmReview, ReviewMark],
    )
    await FilmReview.get_motor_collection().create_index(
        [('mark', 1), ('author.id', 1), ('film_id', 1)], unique=True
    )

    await ReviewMark.get_motor_collection().create_index(
        [('author.id', 1), ('review_id', 1)], unique=True
    )
