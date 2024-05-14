from services import BaseService
from uuid import UUID


class BaseWorkerService(BaseService):
    async def send_email(self, user_id: UUID):
        pass
