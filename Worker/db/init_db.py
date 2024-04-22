from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from models.messages import Message


async def init(*, client: AsyncIOMotorClient) -> None:
    await init_beanie(
        database=getattr(client, settings.mongo.name),
        document_models=[Message],
    )
