from uuid import UUID
from pydantic import BaseModel, Field


class JWTUserData(BaseModel):
    login: str
    uuid: UUID
    roles: list[str] | None = Field(None)
    surname: str | None = Field(None)
    name: str | None = Field(None)
