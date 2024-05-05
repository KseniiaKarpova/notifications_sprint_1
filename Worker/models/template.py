from datetime import date
from typing import Annotated
from fastui.forms import Textarea, fastui_form
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
import enum
from uuid import UUID
from beanie import Document
from models import BaseMixin

class TypeMessage(str, enum.Enum):
    email = 'email'
    notify = 'notify'

class EventMessage(str, enum.Enum):
    like = 'like'
    dislike = 'dislike'
    registration = 'registration'
    info = 'info' #рассылка сообщений


class LoginForm(BaseModel):
    email: EmailStr = Field(
        title='Email Address', description='Enter whatever value you like', json_schema_extra={'autocomplete': 'email'}
    )
    password: SecretStr = Field(
        title='Password',
        description='Enter whatever value you like, password is not checked',
        json_schema_extra={'autocomplete': 'current-password'},
    )

class TemplateModel(BaseMixin, Document):
    template_id: UUID
    name: str | None = Field(None) #Название шаблона
    template: str | None = Field(None) #шаблон сообщения. Используйтся {user} в шаблоне для отображения имени клиента и {redirectUrl} для ссылки
    event: list[EventMessage] | None = Field(None)  #типы событий по которому надо отправить сообщение
    type: list[TypeMessage] | None = Field(None)  #тип канала куда отправить сообщение
    redirectUrl: str | None = Field(None) #ссылка которую подствляют вместо {redirectUrl}
    expirationTimestamp: int | None = Field(None) #redirectUrl нужно переделть в короткую,это описано в теории
    date: date | None = Field(None) # дата для одноразовых рассылок
    schedule: str | None = Field(None) # cron

    class Settings:
        name = "template"
        use_state_management = True


class FormModel(BaseModel):
    name: str = Field(description='Название шаблона')
    template: Annotated[str, Textarea(rows=30)] = Field(None, description='Напишите шаблон сообщения. Используйте {user} в шаблоне для отображения имени клиента и {redirectUrl} для ссылки.')
    event: list[EventMessage] | None = Field(None, title='Отправить сообщение по событию?')
    type: list[TypeMessage] | None = Field(None, title='В какой канал отправить?')
    redirectUrl : str | None = Field(None, description='Ссылка куда перейти')
    expirationTimestamp : int | None = Field(None, description="срок действия ссылки (в часах)")
    date: date | None = Field(None, title='Когда отпавить сообщение?', description='Выбери дату для одноразовой рассылки')
    schedule: str | None = Field(
        None, description='cron format = (* * * * *)'
    )

    @field_validator('template')
    def template_validator(cls, v: str ) -> str:
        #if "{user}" not in v and ('{' in v or '}' in v):
        #   raise PydanticCustomError('user', 'Ваш шаблон не соответвует стандарту. Для автозамены имени пользователя - используйте {user} и {redirectUrl}')
        return v

    @field_validator('schedule')
    def cron_validator(cls, v: str | None) -> str:
        if v is not None:
            return v
            #raise PydanticCustomError('cron', 'Ваш шаблон не соответвует стандарту. используйте (* * * * *)')
        return v