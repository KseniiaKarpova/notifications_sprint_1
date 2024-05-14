from services import BaseService
from uuid import UUID
from core.config import settings
from aiohttp import ClientSession
from core.handlers import AuthHandler, JwtHandler, get_auth_handler, require_refresh_token
from schemas.auth import UserLogin, LoginResponseSchema
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session


class BroadcastService(BaseService):
    def __init__(
            self, auth: AuthHandler) -> None:
        self.auth = auth

    def super_user_tokens(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tokens = await self.auth.user_tokens(
                credentials=UserLogin(
                    login=settings.admin.login,
                    password=settings.admin.password))
            return await func(*args, **kwargs, tokens=tokens)
        return wrapper

    @super_user_tokens
    async def send_email(self, tokens: LoginResponseSchema, user_id: UUID):
        print(user_id, '###########')
        session = ClientSession(headers = {'Authorization': f'Bearer {tokens.access_token}'})
        await session.close()
