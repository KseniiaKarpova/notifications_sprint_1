import asyncio
import logging

import typer
from core import config
from core.hasher import DataHasher
from db import postgres
from sqlalchemy import QueuePool
from sqlalchemy.orm import sessionmaker
from storages.user import UserStorage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import IntegrityError


settings = config.APPSettings()
logging.getLogger('asyncio').setLevel(logging.WARNING)


def create(login: str, password: str, email: str):
    async def save():
        postgres.async_engine = create_async_engine(
            settings.db_dsn,
            poolclass=QueuePool,
            pool_pre_ping=True, pool_size=20, pool_timeout=30)

        postgres.async_session_factory = sessionmaker(
            postgres.async_engine,
            expire_on_commit=False,
            autoflush=True,
            class_=AsyncSession)

        hashed_password = await DataHasher().generate_word_hash(secret_word=password)
        async with postgres.async_session_factory() as session:
            storage = UserStorage(commit_mode=False)
            instance = await storage.create(params={
                'password': hashed_password,
                'login': login,
                'is_superuser': True,
                'email': email,  
            })
            session.add(instance)
            try:
                await session.commit()
            except IntegrityError:
                return await postgres.async_engine.dispose()
        await postgres.async_engine.dispose()
    asyncio.run(save())
    print(f"Creating Super User: {login}")


if __name__ == "__main__":
    typer.run(create)
