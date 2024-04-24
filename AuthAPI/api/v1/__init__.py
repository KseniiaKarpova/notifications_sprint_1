from fastapi import APIRouter

from api.v1 import role, user_history, socials, auth, user


v1_router = APIRouter(prefix='/v1')

v1_router.include_router(role.router, tags=['role'])
v1_router.include_router(user_history.router, tags=['User history'])
v1_router.include_router(socials.router, tags=['socials'])
v1_router.include_router(auth.router, tags=['auth'])
v1_router.include_router(user.router, tags=['user'])
