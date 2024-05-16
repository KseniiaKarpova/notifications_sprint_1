from storages.template import TemplateStorage
from storages.history import HistoryStorage
from models.messages import LogMessage
from models.template import TemplateModel
from services import BaseService
from services.auth import AuthService, super_user_login_required
from uuid import UUID
from datetime import datetime
from models import TypeMessage
from core.config import settings
from aiohttp import ClientSession
from models import TypeMessage, EventMessage



class WebsocketService(BaseService):
    @super_user_login_required
    async def notify(self, user_id: UUID, text: str, access_token: str):
        session = ClientSession(headers = {'Authorization': f'Bearer {access_token}'})
        async with session.post(
            url=settings.websocket.send_message_url,
            json={
                'user_id': str(user_id),
                'text': text
            }) as response:
            json_data = await response.json()
        await session.close()
        return json_data


class EventHandlerService(BaseService):
    def __init__(
            self,
            storage: TemplateStorage,
            logger: HistoryStorage,
            ws_notifier: WebsocketService,
            auth_service: AuthService,
            email: bool = False
            ) -> None:
        self.storage = storage
        self.ws_notifier = ws_notifier
        self.logger = logger
        self.auth_service = auth_service
        self.email = email

    async def proceed(self, sender_id: UUID, reciver_id: UUID, event: str):
        template_obj = await self.storage.get(event=event, type=TypeMessage.notify.value)
        user = await self.auth_service.get_user_by_id(user_id=sender_id)
        text_to_send = await self.compile_text(
            name=user.get('name'), surname=user.get('surname'), template=template_obj.template)
        await self.send_notification(user_id=reciver_id, text=text_to_send)

    async def mass_notification(self, template: str):
        get = True
        page = 1
        while get is True:
            response: dict = await self.auth_service.get_users(page=page, size=100)
            page += 1
            users = response.get('items')
            if not users:
                get = False
            await self.notify_users(users=users, template=template)

    async def notify_users(self, users: list, template: str):
        for user in users:
            text_to_send = await self.compile_text(
                name=user.get('name'), surname=user.get('surname'), template=template)
            await self.send_notification(user_id=user['uuid'], text=text_to_send)

    async def compile_text(self, name: dict, surname: str, template: str):
        name = ''.join(name) if name else ''
        name.join(surname) if surname else ''
        return template.format(user=name)

    async def send_notification(self, user_id: UUID, text):
        await self.logger.add(data=LogMessage(
            user=user_id,
            type=TypeMessage.notify.value,
            text=text,
        ))
        await self.ws_notifier.notify(user_id=user_id, text=text)
        if self.email is True:
            ## тут нужно вызвать нужного метода
            ## который отправит письмо в почту
            pass



def get_event_service():
    return EventHandlerService(
        storage=TemplateStorage(),
        ws_notifier=WebsocketService(),
        auth_service=AuthService(),
        logger=HistoryStorage(),
    )
