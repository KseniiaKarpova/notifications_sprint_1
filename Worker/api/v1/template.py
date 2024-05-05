from fastapi import APIRouter, status, Body, Depends
from services.template import get_template_service, BaseTemplateService
from models.template import TemplateModel
from uuid import UUID

router = APIRouter(prefix='/template', tags=['Template'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=TemplateModel)
async def create_template(
        data: TemplateModel = Body(),
        service: BaseTemplateService = Depends(get_template_service)):
    return await service.add(data=data)