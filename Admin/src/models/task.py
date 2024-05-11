from typing import Annotated
from fastui.forms import Textarea, fastui_form
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
import enum


class TypeMessage(str, enum.Enum):
    email = 'email'
    notify = 'notify'


class EventMessage(str, enum.Enum):
    like = 'like'
    dislike = 'dislike'
    registration = 'registration'
    info = 'info'  # рассылка сообщений


class TemplateModel(BaseModel):
    name: str = Field(description='Название шаблона')
    template: Annotated[str, Textarea(rows=30)] = Field(
        None, description='Напишите шаблон сообщения. Используйте {user} в шаблоне для отображения имени клиента и {redirectUrl} для ссылки.')
    event: list[EventMessage] | None = Field(None, title='Отправить сообщение по событию?')
    type: list[TypeMessage] | None = Field(None, title='В какой канал отправить?')
    redirectUrl: str | None = Field(None, description='Ссылка куда перейти')
    expirationTimestamp: int | None = Field(None, description="срок действия ссылки (в часах)")
