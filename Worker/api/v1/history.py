from fastapi import APIRouter, status, Body, Depends
from services.history import get_history_service, BaseHistoryService
from models.messages import LogMessage
from core.handlers import require_access_token, JwtHandler
from typing import List


router = APIRouter(prefix='/history', tags=['History'])


@router.get('', status_code=status.HTTP_200_OK, response_model=List[LogMessage])
async def create_template(
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: BaseHistoryService = Depends(get_history_service)):
    data = await jwt_handler.get_current_user()
    if data:
        return await service.get(id=data.uuid)
