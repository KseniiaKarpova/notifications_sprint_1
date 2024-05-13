from storages.template import TemplateStorage
from storages.history import HistoryStorage
from models.messages import LogMessage
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
    async def notify_user(self, user_id: UUID, text: str, access_token: str):
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

    async def proceed(self, sender_id: UUID, reciver_id: UUID,event: str):
        template_obj = await self.storage.get(event=event, type=TypeMessage.notify.value)
        user_data = await self.auth_service.get_user_by_id(user_id=sender_id)

        user_name = user_data.get('name')
        user_surname = user_data.get('surname')
        name = ''.join(user_name) if user_name else ''
        name.join(user_surname) if user_surname else ''
        text_to_send = template_obj.template.format(user=name)
        print(text_to_send)
        await self.logger.add(data=LogMessage(
            user=reciver_id,
            type=TypeMessage.notify.value,
            text=text_to_send,
        ))
        await self.ws_notifier.notify_user(user_id=reciver_id, text=text_to_send)


def get_event_service():
    return EventHandlerService(
        storage=TemplateStorage(),
        ws_notifier=WebsocketService(),
        auth_service=AuthService(),
        logger=HistoryStorage(),
    )