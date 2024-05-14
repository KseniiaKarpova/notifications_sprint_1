from functools import lru_cache
from fastapi import Depends
from core.hasher import DataHasher
from services import BaseService
from services.broadcast import BroadcastService
from storages.user import UserStorage
from schemas.auth import UserCredentials
from exceptions import user_created
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session
from core.config import settings
from core.handlers import AuthHandler
from async_fastapi_jwt_auth import AuthJWT


class AuthService(BaseService):
    def __init__(self, 
                 storage: UserStorage, 
                 broadcast: BroadcastService = None):
        self.storage = storage
        self.broadcast = broadcast

    async def registrate(self, data: UserCredentials):
        hashed_password = await DataHasher().generate_word_hash(secret_word=data.password)
        self.storage.commit_mode = False
        user = await self.storage.create(params={
            'password': hashed_password,
            'login': data.login,
            'email': data.email,
        })
        await self.broadcast.send_email(user_id=user.uuid)
        await self.storage.add_and_commit([user])
        return user_created

    async def registrate_super_user(self, data: UserCredentials):
        hashed_password = await DataHasher().generate_word_hash(secret_word=data.password)
        await self.storage.create(params={
            'password': hashed_password,
            'login': data.login,
            'email': data.email,
            'is_superuser': True
        })
        return user_created

    async def is_super_user(self, login):
        status = await self.storage.exists(conditions={
            'login': login,
            'is_superuser': True
        })
        return status
    
    async def get_superuser(self):
        return await self.storage.get(conditions={
            'login': settings.admin.login,
            'email': settings.admin.email,
        })


@lru_cache()
def get_auth_service(
    session: AsyncSession = Depends(create_async_session),
    auth: AuthJWT = Depends(),
) -> AuthService:
    auth_handler = AuthHandler(session=session, Authorize=auth)
    broadcast = BroadcastService(auth=auth_handler)
    return AuthService(storage=UserStorage(session=session), broadcast=broadcast)
