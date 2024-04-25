from utils.constraint import RequestLimit
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from api import setup_routers
from core.config import settings
from db import mongo, init_db, redis
from redis.asyncio import Redis
from core.logger import LOGGING, setup_root_logger
from middleware.main import setup_middleware
import sentry_sdk

setup_root_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    sentry_sdk.init(
        dsn=settings.logger.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    mongo.mongo_client = AsyncIOMotorClient(str(settings.mongodb.uri), uuidRepresentation='standard')
    await init_db.init(client=mongo.mongo_client)
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    yield
    mongo.mongo_client.close()
    await redis.redis.close()


def create_app() -> FastAPI:
    application = FastAPI(
        lifespan=lifespan,
        title='Post creator',
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        description='Orders Service',
        version='0.1.0',
    )

    setup_routers(application)
    setup_middleware(application)
    add_pagination(application)
    return application


app = create_app()


@app.middleware('http')
async def before_request(request: Request, call_next):
    user = request.headers.get('X-Forwarded-For')
    result = await RequestLimit().is_over_limit(user=user)
    if result:
        return ORJSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={
                'detail': 'Too many requests'
                }
            )

    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if settings.jaeger.enable is False:
        return response
    request_id = request.headers.get('request_id')
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                'detail': 'X-Request-Id is required'
                })
    return response


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=settings.log_level,
        reload=True,
    )
