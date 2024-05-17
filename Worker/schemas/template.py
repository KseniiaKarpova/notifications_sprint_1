from pydantic import BaseModel, Field
from datetime import date
from models import TypeMessage, EventMessage


class TemplateSchema(BaseModel):
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
