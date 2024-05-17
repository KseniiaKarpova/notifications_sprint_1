from pydantic import BaseModel, Field
from uuid import UUID


class Message(BaseModel):
    sender_id: UUID
    reciver_id: UUID


class LikeDislike(BaseModel):
    user_id: UUID
    review_id: UUID
    mark: int = Field(ge=0, le=10)


class EventSchema(BaseModel):
    # if all the fields are None then the new film added
    reciver_id: UUID | None = Field(None, description='the user who should be notified')
    sender_id: UUID | None = Field(None, description='the user who made event')
    # these fields below for like and dislike events
    # that is why they are optional
    review_id: UUID | None = Field(None, description="the film's review")
    film_id: UUID | None = Field(None, description="the film's id")


class InfoSchema(BaseModel):
    film_id: UUID | None = Field(None, description="the film's id")


class EventHandlerSchema(BaseModel):
    type: str | None = Field(..., examples=['like', 'dislike', 'registration'])
    data: EventSchema
