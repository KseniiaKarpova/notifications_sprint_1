from uuid import UUID
from beanie import Document
from pydantic import Field
from models import BaseMixin


class Message(BaseMixin, Document):
    sender_id: UUID
    reciver_id: UUID
    text: str

    class Settings:
        name = "message"
        use_state_management = True
