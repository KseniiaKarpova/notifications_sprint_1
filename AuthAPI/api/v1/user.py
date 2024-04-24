from core.handlers import JwtHandler, require_access_token
from fastapi import APIRouter, Body, Depends
from schemas.auth import UserUpdate
from services.user import get_user_service, UserService
from uuid import UUID
from fastapi_pagination import Page
from schemas.auth import UserData

router = APIRouter(prefix="/user")


@router.get("/{user_id}", response_model=UserData)
async def get_user(
        user_id: UUID,
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: UserService = Depends(get_user_service),
        ):
    current_user = await jwt_handler.get_current_user()
    return await service.get_user(uuid=current_user.uuid)


@router.get("", response_model=Page[UserData])
async def get_users(
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: UserService = Depends(get_user_service)
        ):
    await jwt_handler.is_super_user()
    return await service.get_users()


@router.patch("")
async def update_user(
        user_data: UserUpdate = Body(),
        jwt_handler: JwtHandler = Depends(require_access_token),
        service: UserService = Depends(get_user_service),
        ):
    current_user = await jwt_handler.get_current_user()
    return await service.update_user(data=user_data, user_id=current_user.uuid)
