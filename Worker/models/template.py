from datetime import date
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
from beanie import Document
from models import BaseMixin
from models import TypeMessage, EventMessage
from fastapi import HTTPException, status
import re


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
    name: str = Field(description='Название шаблона')
    template: str = Field(
        None,
        description='Напишите шаблон сообщения. Используйте {user} в шаблоне для отображения имени клиента и {redirectUrl} для ссылки.')
    event: str | None = Field(
        None,
        title='Отправить сообщение по событию?',
        examples=[
            EventMessage.like.value,
            EventMessage.dislike.value,
            EventMessage.registration.value])
    type: str | None = Field(None, title='В какой канал отправить?', examples=[
                             TypeMessage.email.value, TypeMessage.notify.value])
    redirectUrl: str | None = Field(None, description='Ссылка куда перейти')
    expirationTimestamp: int | None = Field(None, description="срок действия ссылки (в часах)")
    date_send: date | None = Field(None, title='Когда отпавить сообщение?', description='Выбери дату для одноразовой рассылки')
    schedule: str | None = Field(
        None, description='Требуется повторить рассылку? Укажи как часто: "ДеньНедели Мес День Час минуты"'
    )

    class Settings:
        name = "template"
        use_state_management = True

    @field_validator('template')
    def template_validator(cls, v: str) -> str:
        if "{user}" not in v and "{redirectUrl}" not in v:
            if '{' in v or '}' in v:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Ваш шаблон не соответвует стандарту. Для автозамены имени пользователя - используйте {user} и {redirectUrl}')
        return v

    @field_validator('schedule')
    def cron_validator(cls, v: str) -> str:
        cron_pattern = r'^(\*|\d+)\s(\*|\d+)\s(\*|\d+)\s(\*|\d+)\s(\*|\d+)$'
        if not v:
            return v
        if not bool(re.match(cron_pattern, v)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Ваш шаблон не соответвует стандарту "Г М Д Ч м". Пример: "* * * 1 *" - каждый час')

        return v
