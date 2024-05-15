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
            ) -> None:
        self.storage = storage
        self.ws_notifier = ws_notifier
        self.logger = logger
        self.auth_service = auth_service

    async def proceed(self, sender_id: UUID, reciver_id: UUID, event: str):
        template_obj = await self.storage.get(event=event, type=TypeMessage.notify.value)
        user_data = await self.auth_service.get_user_by_id(user_id=sender_id)
        text_to_send = await self.compile_text(user=user_data, template=template_obj.template)
        await self.ws_notifier.notify(user_id=reciver_id, text=text_to_send)

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
            text_to_send = await self.compile_text(user=user, template=template)
            await self.ws_notifier.notify(user_id=user['uuid'], text=text_to_send)
            await self.logger.add(data=LogMessage(
                user=user['uuid'],
                type=TypeMessage.notify.value,
                text=text_to_send,
            ))

    async def compile_text(self, user: dict, template: str):
        user_name = user.get('name')
        user_surname = user.get('surname')
        name = ''.join(user_name) if user_name else ''
        name.join(user_surname) if user_surname else ''
        return template.format(user=name)


def get_event_service():
    return EventHandlerService(
        storage=TemplateStorage(),
        ws_notifier=WebsocketService(),
        auth_service=AuthService(),
        logger=HistoryStorage(),
    )
