from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter, Logger
from faststream.rabbit import RabbitBroker
from core.config import settings
from schemas import EventSchema, InfoSchema, EventHandlerSchema
from models import EventMessage, InfoMessage
from services.events import get_event_service, EventHandlerService
from core.handlers import require_access_token, JwtHandler


router = RabbitRouter(settings.rabbit.dsn)


def broker():
    return router.broker


@router.subscriber(queue='event_handler')
async def event_handler(
        message: EventHandlerSchema, logger: Logger,
        service: EventHandlerService = Depends(get_event_service)):
    await service.proceed(sender_id=message.data.sender_id, event=message.type, reciver_id=message.data.reciver_id)


@router.subscriber(queue='info')
async def info(message: InfoSchema, logger: Logger):
    message = message.model_dump(exclude_none=True, exclude_unset=True)


@router.subscriber(queue='film_added')
async def film_added(message: InfoSchema, logger: Logger):
    message = message.model_dump(exclude_none=True, exclude_unset=True)


@router.post("/{event}")
async def _event(
        event: EventMessage,
        data: EventSchema | None = None,
        broker: RabbitBroker = Depends(broker),
        jwt_handler: JwtHandler = Depends(require_access_token)):
    current_user = await jwt_handler.is_superuser()
    handler_data = EventHandlerSchema(
        type=event,
        data=data.model_dump(exclude_none=True, exclude_unset=True),
    )
    return await broker.publish(queue='event_handler', message=handler_data)


@router.post("/{info}")
async def _info(
        info: InfoMessage,
        data: InfoSchema,
        broker: RabbitBroker = Depends(broker)):
    return await broker.publish(queue=info, message=data)
