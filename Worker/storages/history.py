from models.messages import LogMessage
from storages import BaseStorage
from beanie import Document
from pymongo.errors import DuplicateKeyError
from exceptions import already_exists, deleted
from uuid import UUID


class HistoryStorage(BaseStorage):
    document: Document = LogMessage

    async def add(self, data: LogMessage):
        try:
            return await data.create()
        except DuplicateKeyError:
            raise already_exists

    async def get(self, **kwargs):
        return await LogMessage.find_many(kwargs)

    async def delete(self, id: UUID):
        await self.document.find({'_id': id}).delete()
        return deleted

    async def update(self, id: UUID, data: LogMessage):
        return await self.document.find_one({'_id': id}).update(
            {"$set": data.model_dump(exclude_none=True, exclude_unset=True)})
