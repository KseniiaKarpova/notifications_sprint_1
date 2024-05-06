from fastapi import APIRouter, Depends
from services.connection import get_manager, ConnectionManager
from uuid import UUID

router = APIRouter(tags=['Send message'])


@router.post(
    "/send",
    response_description="send message",
    description="",
    status_code=200
)
async def upload_file(
    user_id: UUID,
    text: str,
    ws_service: ConnectionManager = Depends(get_manager)
):
    await ws_service.send_personal_message(user_id, text)