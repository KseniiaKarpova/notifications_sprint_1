from storages.template import TemplateStorage
from storages.history import HistoryStorage
from models.messages import LogMessage
from services import BaseService
from abc import abstractmethod
from fastapi import Depends
from uuid import UUID


class BaseHistoryService(BaseService):
    def __init__(
            self,
            storage: TemplateStorage,
            dto: LogMessage = None) -> None:
        self.storage = storage
        self.dto = dto

    @abstractmethod
    async def add(self, data: LogMessage):
        pass

    @abstractmethod
    async def get(self, id: UUID):
        pass



class HistoryService(BaseHistoryService):

    async def get(self, id: UUID):
        return await self.storage.get(user=id)

    async def add(self, data: LogMessage):
        return await self.storage.add(data=data)


def get_history_service(
        storage: HistoryStorage = Depends(HistoryStorage),
        ) -> BaseHistoryService:
    return HistoryService(storage=storage)

def get_logger(storage: HistoryStorage = HistoryStorage()) -> BaseHistoryService:
    return HistoryService(storage=storage)