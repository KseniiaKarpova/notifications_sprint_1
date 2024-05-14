from uuid import UUID
from beanie import Document
from models import BaseMixin
from datetime import date
from models import TypeMessage
from pydantic import Field, BaseModel
from typing import List
from jinja2 import Environment

class Message(BaseMixin, Document):
    sender_id: UUID
    reciver_id: UUID
    text: str

    class Settings:
        name = "message"
        use_state_management = True


class LogMessage(BaseMixin, Document):
    dt: date = Field(default_factory=lambda: date.today())
    user: UUID
    type: TypeMessage
    text: str

    class Settings:
        name = "history"
        use_state_management = True


class Email(BaseModel):
    To: List[str]
    Subject: str = 'Онлайн кинотеатр'
    Message : Environment