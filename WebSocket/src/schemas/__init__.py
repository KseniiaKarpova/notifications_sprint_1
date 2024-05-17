from pydantic import BaseModel
from uuid import UUID


class SendMessageSchema(BaseModel):
    user_id: UUID
    text: str
