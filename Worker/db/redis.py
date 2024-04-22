from core.config import settings
from redis.asyncio import Redis

redis: Redis | None = Redis(host=settings.redis.host, port=settings.redis.port)


def get_redis() -> Redis | None:
    return redis
