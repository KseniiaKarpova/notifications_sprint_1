from pydantic import Field, BaseModel
from datetime import datetime, timezone
from uuid import UUID, uuid4
import enum


class TypeMessage(str, enum.Enum):
    email = 'email'
    notify = 'notify'


class EventMessage(str, enum.Enum):
    like = 'like'
    dislike = 'dislike'
    registration = 'registration'


class BaseMixin(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InfoMessage(str, enum.Enum):
    film_added = 'film_added'
    info = 'info'
