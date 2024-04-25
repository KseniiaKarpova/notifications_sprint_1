import asyncio

import pytest_asyncio
from aiohttp import ClientSession
from functional.settings import test_settings

user_create = {
            "login": "test_login",
            "password": "test_password",
            "email": "test_email"}

user_login = {
            "login": "test_login",
            "password": "test_password",
            "agent": "test_device"}


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='aiohttp_session', scope='session')
async def aiohttp_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name='make_post_request')
def make_post_request(aiohttp_session: ClientSession):
    async def inner(endpoint, service_url, json, headers=None):
        url = f"{service_url}{endpoint}"
        async with aiohttp_session.post(url, json=json, headers=headers) as response:
            json_data, status_code = await response.json(), response.status
        return json_data, status_code
    return inner


@pytest_asyncio.fixture(name='get_access_token')
def get_access_token(aiohttp_session: ClientSession):
    reg_url = f"{test_settings.auth_service_url}/api/v1/auth/registration"
    login_url = f"{test_settings.auth_service_url}/api/v1/auth/login"

    async def inner():
        async with aiohttp_session.post(reg_url, json=user_create) as response:
            json_data, _ = await response.json(), response.status
        async with aiohttp_session.post(login_url, json=user_login) as response:
            json_data, _ = await response.json(), response.status
        return json_data['access_token']
    return inner
