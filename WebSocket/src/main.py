from uuid import UUID
from services.connection import get_manager, ConnectionManager
from fastapi import Depends, WebSocket, WebSocketDisconnect
from core.handlers import require_access_token, JwtHandler
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from db import redis
from contextlib import asynccontextmanager
from services import connection
from core.config import settings
from api import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    connection.connects_manager = connection.ConnectionManager()
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    yield
    await redis.redis.close()
app = FastAPI(
    lifespan=lifespan,
    description="WebSocket notify services",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(router, prefix='/api/v1')


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(
        websocket: WebSocket, user_id: UUID,
        jwt_handler: JwtHandler = Depends(require_access_token),
        manager: ConnectionManager = Depends(get_manager)):
    await jwt_handler.get_current_user()
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(
                f"You: {data}"
            )
    except WebSocketDisconnect:
        manager.disconnect(user_id)
