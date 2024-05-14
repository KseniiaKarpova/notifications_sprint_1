from pydantic import BaseModel, Field
from uuid import UUID


class SendMessageSchema(BaseModel):
    user_id: UUID
    text: str
