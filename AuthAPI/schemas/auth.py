from datetime import timedelta
from uuid import UUID

from core.config import settings
from core.hasher import DataHasher
from pydantic import BaseModel, Field, validator
from core.hasher import fake
import re


class EmailValidator:
    EMAIL_REGEX = re.compile(
        r"^(?=.{1,256})(?=.{1,64}@.{1,255}$)(?=\S)([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,})$"
    )

    @staticmethod
    def is_valid(email: str) -> bool:
        return re.match(EmailValidator.EMAIL_REGEX, email) is not None


class UserCredentials(BaseModel):
    login: str | None = Field(None, description="login")
    password: str
    email: str

    @validator('email')
    def validate_email(cls, value):
        if not EmailValidator.is_valid(value):
            raise ValueError('Invalid email address')
        return value


class UserLogin(BaseModel):
    login: str
    password: str
    agent: str


class UserAuthData(BaseModel):
    email: str | None = Field(None, description="email")
    surname: str | None = Field(None, description="surname")
    name: str | None = Field(None, description="name")

    @validator("email")
    def email_generating(cls, value):
        if not value:
            return fake.ascii_company_email()
        return value

    @validator("surname")
    def surname_generating(cls, value):
        if not value:
            return fake.last_name()
        return value

    @validator("name")
    def name_generating(cls, value):
        if not value:
            return fake.first_name()
        return value


class AuthSettingsSchema(BaseModel):
    authjwt_secret_key: str = settings.auth.secret_key
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    authjwt_algorithm: str = "HS256"
    access_expires: int = timedelta(minutes=15)
    refresh_expires: int = timedelta(days=30)


class LoginResponseSchema(BaseModel):
    access_token: str = Field(description='Access token value')
    refresh_token: str | None = Field(None, description='Refresh token value')


class JWTUserData(BaseModel):
    login: str
    uuid: UUID
    roles: list[str] | list[None] = Field(None)
    surname: str | None = Field(None)
    name: str | None = Field(None)
    is_superuser: bool | None = Field(None)


class UserUpdate(BaseModel):
    password: str = Field(None, description="new login")
    login: str = Field(None, description="new password")

    @validator("password")
    def hash_pass(cls, value):
        if not value:
            return None
        return DataHasher().sync_generater(secret_word=value)


class SocialData(BaseModel):
    user: UserAuthData
    social_user_id: str
    type: str
    data: dict


class UserData(BaseModel):
    uuid: UUID
    email: str
    name: str | None
    surname: str | None
