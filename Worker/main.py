from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse, JSONResponse
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from api.v1.notifications import router
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from db import mongo, init_db, redis
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
from api.v1.template import router as template_router
from api.v1.history import router as history_router
from services.periodic_notify import send_periodic_notify
import smtplib
from services import email_sender


@asynccontextmanager
async def custom_lifespan_context(_: FastAPI):
    mongo.mongo_client = AsyncIOMotorClient(str(settings.mongo.uri), uuidRepresentation='standard')
    await init_db.init(client=mongo.mongo_client)
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    await router.broker.start()
    await send_periodic_notify()
    email_sender.server = smtplib.SMTP_SSL(settings.smpt.host, settings.smpt.port)

    yield
    mongo.mongo_client.close()
    await router.broker.close()
    await redis.redis.close()
    email_sender.server.close()

app = FastAPI(
    lifespan=custom_lifespan_context,
    description="Notification logic",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    )


app.include_router(router, prefix='/api/v1')
app.include_router(template_router, prefix='/api/v1')
app.include_router(history_router, prefix='/api/v1')


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={
            "detail": exc.message})

