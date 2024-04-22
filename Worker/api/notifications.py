from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter, Logger
from faststream.rabbit import RabbitBroker
from core.config import settings
from schemas import LikeDislike

router = RabbitRouter(settings.rabbit_dsn)

def broker():
    return router.broker


@router.subscriber("mark_review")
async def save_message(content: LikeDislike, logger: Logger):
    return {"response": "Hello, Rabbit!"}


@router.subscriber("registration")
async def save_message(content: LikeDislike, logger: Logger):
    return {"response": "Hello, Rabbit!"}


@router.post("")
async def message(
        broker: RabbitBroker = Depends(broker)):
    return await broker.publish(queue="liked", message="sdadasdsd")
