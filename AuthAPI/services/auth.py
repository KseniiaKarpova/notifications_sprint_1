from functools import lru_cache
from fastapi import Depends
from core.hasher import DataHasher
from services import BaseService
from storages.user import UserStorage
from schemas.auth import UserCredentials
from exceptions import user_created
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import create_async_session


class AuthService(BaseService):
    def __init__(self, storage: UserStorage):
        self.storage = storage

    async def registrate(self, data: UserCredentials):
        hashed_password = await DataHasher().generate_word_hash(secret_word=data.password)
        await self.storage.create(params={
            'password': hashed_password,
            'login': data.login,
            'email': data.email,
        })
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


@lru_cache()
def get_auth_service(
    session: AsyncSession = Depends(create_async_session)
) -> AuthService:
    return AuthService(storage=UserStorage(session=session))
