from services import BaseService
from uuid import UUID
from aiohttp import ClientSession
from core.config import settings
from functools import wraps


def super_user_login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with ClientSession() as session:
            credentials = {
                'login': settings.admin.login,
                'password': settings.admin.password,
                'agent': 'test browser)'
            }
            async with session.post(url=f"{settings.auth.api_url}/auth/login", json=credentials) as response:
                if response.status != 200:
                    raise Exception("Auth Login failed")
                json_data = await response.json()
                if json_data:
                    return await func(*args, **kwargs, access_token=json_data.get('access_token'))
    return wrapper


class AuthService(BaseService):
    @super_user_login_required
    async def get_user_by_id(self, user_id: UUID, access_token: str) -> dict:
        session = ClientSession(headers={'Authorization': f'Bearer {access_token}'})
        async with session.get(url=f"{settings.auth.api_url}/user/{user_id}") as response:
            json_data = await response.json()
        await session.close()
        return json_data

    @super_user_login_required
    async def get_users(self, page: int, size: int, access_token: str):
        session = ClientSession(headers = {'Authorization': f'Bearer {access_token}'})
        async with session.get(url=f"{settings.auth.api_url}/user?page={page}&size={size}") as response:
            json_data = await response.json()
        await session.close()
        return json_data
