from fastapi import APIRouter, status, Body, Depends
from services.template import get_template_service, BaseTemplateService
from services.auth import AuthService
from models.template import TemplateModel
from core.handlers import require_access_token, JwtHandler


router = APIRouter(prefix='/template', tags=['Template'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=TemplateModel)
async def create_template(
        data: TemplateModel = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: BaseTemplateService = Depends(get_template_service)):
    current_user = await jwt_handler.is_superuser()
    await AuthService().get_user_by_id(user_id=current_user.uuid)
    return await service.add(data=data)
