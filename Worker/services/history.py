from storages.template import TemplateStorage
from services import BaseService
from abc import abstractmethod
from fastapi import Depends
from storages.history import HistoryStorage
from uuid import UUID


class BaseHistoryService(BaseService):
    def __init__(
            self,
            storage: TemplateStorage,
            dto: HistoryStorage = None) -> None:
        self.storage = storage
        self.dto = dto

    @abstractmethod
    async def add(self, data: HistoryStorage):
        pass

    @abstractmethod
    async def get(self, id: UUID):
        pass



class HistoryService(BaseHistoryService):

    async def get(self, id: UUID):
        return await self.storage.get(user=id)

    async def add(self, data: HistoryStorage):
        pass


def get_history_service(
        storage: HistoryStorage = Depends(HistoryStorage),
        ) -> BaseHistoryService:
    return HistoryService(storage=storage)