import asyncio
import logging

import typer
from core import config
from core.hasher import DataHasher
from db import postgres
from storages.user import UserStorage


settings = config.APPSettings()
logging.getLogger('asyncio').setLevel(logging.WARNING)


def create(login: str, password: str, email: str):
    async def save():
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
            await session.commit()
    asyncio.run(save())
    print(f"Creating Super User: {login}")

if __name__ == "__main__":
    typer.run(create)
