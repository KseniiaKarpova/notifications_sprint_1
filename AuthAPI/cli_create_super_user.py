import asyncio
import logging

import typer
from core import config
from core.hasher import DataHasher
from models.models import User
from db import postgres
from sqlalchemy import create_engine, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from storages.user import UserStorage


settings = config.APPSettings()
logging.getLogger('asyncio').setLevel(logging.WARNING)


def create(login: str, password: str):
    try:
        async def save():
            engine = create_engine(settings.db_dsn)
            hashed_password = await DataHasher().generate_word_hash(secret_word=password)
            factory = sessionmaker(bind=engine)
            session = factory()
            new_rec = User(password=hashed_password,
                           login=login,
                           email='',
                           is_superuser=True)
            session.add(new_rec)
            session.commit()

        asyncio.run(save())

        print(f"Creating Super User: {login}")

    except Exception as e:
        print('Can`t create Super User')
        print(e)


if __name__ == "__main__":
    typer.run(create)
