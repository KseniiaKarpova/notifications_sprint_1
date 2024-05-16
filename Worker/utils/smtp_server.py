from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiosmtplib import SMTP
from core.config import settings
from fastapi import Depends

# SMTP client placeholder
client: SMTP | None = SMTP(hostname=settings.smtp.host, port=settings.smtp.port)


async def get_async_client():
    return client


class SmtpServer:
    def __init__(
            self,
            client: SMTP) -> None:
        self.client = client

    async def email(self, reciever: str, text: str,):
        msg = MIMEMultipart()
        msg["From"] = settings.smtp.from_user
        msg["To"] = reciever
        msg["Subject"] = text
        await self.client.send_message(msg)


def get_server(client: SMTP = Depends(get_async_client)):
    return SmtpServer(client=client)
