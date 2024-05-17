from storages import TemplateStorage
from utils import check_now_is_valid_cron
from datetime import datetime


async def send_periodic_notify():
    storage = TemplateStorage()
    data = await storage.get_all()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    for item in data:

        if check_now_is_valid_cron(item.schedule):
            # отправить на рассылку сообщение
            pass

        else:
            d = item.date_send.strftime("%d/%m/%Y %H:%M")
            if d == now:
                # отправить на рассылку сообщение
                pass
