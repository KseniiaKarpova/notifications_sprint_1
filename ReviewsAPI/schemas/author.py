from pydantic import BaseModel, Field
from uuid import UUID


class Author(BaseModel):
    id: UUID
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
