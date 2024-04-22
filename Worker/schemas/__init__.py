from pydantic import BaseModel, Field
from uuid import UUID


class Message(BaseModel):
    sender_id: UUID
    reciver_id: UUID


class LikeDislike(BaseModel):
    user_id: UUID
    review_id: UUID
    mark: int = Field(ge=0, le=10)
