from storages.template import TemplateStorage
from services import BaseService
from abc import abstractmethod
from fastapi import Depends
from models.template import TemplateModel
from uuid import UUID


class BaseTemplateService(BaseService):
    def __init__(
            self,
            storage: TemplateStorage,
            dto: TemplateModel = None) -> None:
        self.storage = storage
        self.dto = dto

    @abstractmethod
    async def add(self, data: TemplateModel):
        pass

    @abstractmethod
    async def get(self, id: UUID):
        pass

    @abstractmethod
    async def set(self, id: UUID, data: TemplateModel):
        pass


class TemplateService(BaseTemplateService):
    async def add(self, data: TemplateModel):
        return await self.storage.add(data=data)

    async def get(self, id: UUID):
        return await self.storage.get(id=id)

    async def set(self, id: UUID, data: TemplateModel):
        return await self.storage.update(id=id, data=data)



def get_template_service(
        storage: TemplateStorage = Depends(TemplateStorage),
        ) -> BaseTemplateService:
    return TemplateService(storage=storage)