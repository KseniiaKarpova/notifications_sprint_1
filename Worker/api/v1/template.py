from fastapi import APIRouter, status, Body, Depends
from services.template import get_template_service, BaseTemplateService
from models.template import TemplateModel
from uuid import UUID
from core.handlers import require_access_token, JwtHandler
from exceptions import unauthorized


router = APIRouter(prefix='/template', tags=['Template'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=TemplateModel)
async def create_template(
        data: TemplateModel = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: BaseTemplateService = Depends(get_template_service)):
    current_user = await jwt_handler.get_current_user()
    if data and current_user.is_superuser:
        return await service.add(data=data)
    else:
        raise unauthorized

