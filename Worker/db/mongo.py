from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends


mongo_client: AsyncIOMotorClient | None = None  # type: ignore


async def get_mongo_client() -> AsyncIOMotorClient:  # type: ignore
    return mongo_client


async def create_mongo_session(client=Depends(get_mongo_client)):
    async with await client.start_session() as session:
        async with session.start_transaction():
            yield session
