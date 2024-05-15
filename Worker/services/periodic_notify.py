from fastapi import Depends
from storages.template import TemplateStorage
from utils import check_now_is_valid_cron
from datetime import datetime
from fastapi_utilities import repeat_every
from api.v1.notifications import router
from faststream.rabbit import RabbitBroker
from core.config import settings
from schemas import InfoSchema


broker = RabbitBroker(settings.rabbit.dsn)


@repeat_every(seconds=20)
async def send_periodic_notify():
    storage = TemplateStorage()
    data = await storage.get_all()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    for item in data:

        if check_now_is_valid_cron(item.schedule):
            #отправить на рассылку сообщение
            await router.broker.publish(queue='info', message=InfoSchema(template=item.template))

        else:
            d = item.date_send.strftime("%d/%m/%Y %H:%M")
            if d==now:
                # отправить на рассылку сообщение
                pass
