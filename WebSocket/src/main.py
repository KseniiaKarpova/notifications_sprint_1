from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from services import connection
from api import router
from uuid import UUID


@asynccontextmanager
async def lifespan(_: FastAPI):
    connection.connects_manager = connection.ConnectionManager()
    yield

app = FastAPI(
    lifespan=lifespan,
    description="WebSocket notify services",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(router, prefix='/api/v1')


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: UUID):
    await connection.get_manager().connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(
                f"You: {data}"
            )
    except WebSocketDisconnect:
        connection.get_manager().disconnect(user_id)
