from services import BaseService
from uuid import UUID
from aiohttp import ClientSession
from core.handlers import AuthHandler


class BroadcastService(BaseService):
    def __init__(
            self, auth: AuthHandler) -> None:
        self.auth = auth

    async def send_email(self, user_id: UUID):
        tokens = await self.auth.login_as_superuser()
        session = ClientSession(headers={'Authorization': f'Bearer {tokens.access_token}'})
        await session.close()
