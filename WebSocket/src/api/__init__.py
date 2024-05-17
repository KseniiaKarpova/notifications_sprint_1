from fastapi import APIRouter, Depends, Body
from services.connection import get_manager, ConnectionManager
from core.handlers import require_access_token, JwtHandler
from services.connection import ConnectionManager
from schemas import SendMessageSchema


router = APIRouter(tags=['Send message'])


@router.post(
    "/send",
    response_description="send message",
    description="",
    status_code=200
)
async def send_message(
    data: SendMessageSchema = Body(),
    ws_service: ConnectionManager = Depends(get_manager),
    jwt_handler: JwtHandler = Depends(require_access_token),
):
    await jwt_handler.get_current_user()
    await ws_service.send_personal_message(data.user_id, data.text)
