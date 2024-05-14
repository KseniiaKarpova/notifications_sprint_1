import json
import time
from typing import Optional

from core.config import settings
from db.redis import get_redis
from exceptions import forbidden_error, wrong_data
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, ExpiredSignatureError
from schemas.auth import JWTUserData
from exceptions import unauthorized, token_expired


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(
            token, settings.auth.secret_key, algorithms=[
                settings.auth.jwt_algorithm])
        if decoded_token['exp'] < time.time():
            raise forbidden_error
        return decoded_token
    except ExpiredSignatureError:
        raise token_expired
    except Exception:
        raise wrong_data


async def jwt_user_data(subject: dict):
    subject: dict = json.loads(subject)
    login, uuid = subject.get('login'), subject.get('uuid')
    if not login or not uuid:
        raise forbidden_error
    return JWTUserData(
        login=login, uuid=uuid,
        is_superuser=subject.get('is_superuser'),
        )


class JWTBearer(HTTPBearer):
    def __init__(
            self, auto_error: bool = True,
            token_type: str = 'access'):
        self.token_type = token_type
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        await self.check_credentials(credentials=credentials)
        decoded_token = decode_token(credentials.credentials)
        subject, jti, type = await self.check_fields(decoded_token=decoded_token)
        if type != self.token_type:
            raise forbidden_error
        return {
            'subject': subject,
            'jti': jti,
            'type': type
        }

    async def check_denylist(self, jti):
        redis = get_redis()
        denied = await redis.get(jti)
        if denied:
            raise forbidden_error

    async def check_credentials(self, credentials: HTTPAuthorizationCredentials):
        if not credentials:
            raise forbidden_error
        if not credentials.scheme == 'Bearer':
            raise unauthorized

    async def check_fields(self, decoded_token: dict):
        subject: dict = decoded_token.get('sub')
        jti = decoded_token.get('jti')
        type = decoded_token.get('type')
        if not subject or not jti or not type:
            raise forbidden_error
        await self.check_denylist(jti=jti)
        return subject, jti, type


class JwtHandler:
    def __init__(self, jwt_data: dict = None) -> None:
        self.jwt_data = jwt_data

    async def get_current_user(self):
        return await jwt_user_data(subject=self.subject)

    @property
    def subject(self):
        return self.jwt_data.get('subject')

    async def is_superuser(self):
        user_data = await jwt_user_data(subject=self.subject)
        if user_data.is_superuser is True:
            return user_data
        raise forbidden_error


def require_access_token(
    jwt_data: dict = Depends(JWTBearer(token_type='access'))
) -> JwtHandler:
    return JwtHandler(jwt_data=jwt_data)
