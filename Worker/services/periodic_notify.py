from storages.template import TemplateStorage
from utils import check_now_is_valid_cron
from datetime import datetime
from fastapi_utilities import repeat_every
from api.v1.notifications import router
from faststream.rabbit import RabbitBroker
from core.config import settings
from services.history import get_logger
from services.email_sender import get_email_services
from models.messages import Email
from models.messages import LogMessage
from models import TypeMessage
from models.template import TemplateModel

broker = RabbitBroker(settings.rabbit.dsn)
logger = get_logger()
email_sender = get_email_services()


def send(item: TemplateModel, email, uuid):

    templ = email_sender.rendering_template(item.template, {
        'user': item.user,
        'redirectUrl': item.redirectUrl
    })
    result = email_sender.send(Email(To=email, Message=templ))
    if result:
        # логируем
        logger.add(
            LogMessage(
                user=uuid,
                type=TypeMessage.email,
                text=result
            )
        )


@repeat_every(seconds=3)
async def send_periodic_notify():
    print('#######started########')
    storage = TemplateStorage()
    data = await storage.get_all()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    await router.broker.publish(queue='info', message='asdsdsds')
    for item in data:

        if check_now_is_valid_cron(item.schedule):
            #получить список адресов и UUID
            emails = []
            UUID = []

            #отправить на рассылку сообщение
            for em, id in zip(emails, UUID):
                send(item,em, id)

        else:
            d = item.date_send.strftime("%d/%m/%Y %H:%M")
            if d==now:
                # получить список адресов и UUID
                emails = []
                UUID = []

                # отправить на рассылку сообщение
                for em, id in zip(emails, UUID):
                    send(item, em, id)
