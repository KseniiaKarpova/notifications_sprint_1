from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from models.messages import Message, LogMessage
from models.template import TemplateModel


async def init(*, client: AsyncIOMotorClient) -> None:
    await init_beanie(
        database=getattr(client, settings.mongo.name),
        document_models=[Message, TemplateModel, LogMessage],
    )
    await TemplateModel.get_motor_collection().create_index(
        [('event', 1), ('type', 1)], unique=True
    )
