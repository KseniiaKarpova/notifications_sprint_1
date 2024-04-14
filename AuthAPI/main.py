import logging
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import auth as auth_api
from api.v1 import role, user_history, socials
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from core import config, logger, oauth2
from db import postgres, redis
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from utils.constraint import RequestLimit
from utils.jaeger import configure_tracer
from authlib.integrations.httpx_client import AsyncOAuth2Client
from middleware.main import setup_middleware


settings = config.APPSettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.jaeger.enable:
        configure_tracer(
            host=settings.jaeger.host,
            port=settings.jaeger.port,
            service_name=settings.project_name)

    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    postgres.async_engine = create_async_engine(
        settings.db_dsn,
        pool_pre_ping=True, pool_size=20, pool_timeout=30)
    postgres.async_session_factory = sessionmaker(
        postgres.async_engine,
        expire_on_commit=False,
        autoflush=True,
        class_=AsyncSession)
    oauth2.google_client = AsyncOAuth2Client(
        client_id=settings.auth.google_client_id,
        client_secret=settings.auth.google_client_secret,
        redirect_uri=settings.auth.google_redirect_url,
        scope='openid email profile')
    yield
    await postgres.async_engine.dispose()
    postgres.async_session_factory.close_all()
    await redis.redis.close()
    await oauth2.google_client.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        description="Auth logic",
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        lifespan=lifespan
    )
    setup_middleware(app)
    app.include_router(
        router=auth_api.router,
        prefix="/api/v1/auth",
        tags=["auth"])
    app.include_router(
        router=role.router,
        prefix="/api/v1/role",
        tags=["role"])
    app.include_router(
        router=user_history.router,
        prefix="/api/v1/user_history",
        tags=["role"])

    app.include_router(
        router=socials.router,
        prefix="/api/v1/socials",
        tags=["social_auth"])
    return app


app = create_app()


FastAPIInstrumentor.instrument_app(app)


@app.middleware('http')
async def before_request(request: Request, call_next):
    user = request.headers.get('X-Forwarded-For')
    result = await RequestLimit().is_over_limit(user=user)
    if result:
        return ORJSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={
                'detail': 'Too many requests'}
        )

    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if settings.jaeger.enable is False:
        return response
    request_id = request.headers.get('request_id')
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                'detail': 'X-Request-Id is required'})
    return response


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={
            "detail": exc.message})


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=logger.LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
