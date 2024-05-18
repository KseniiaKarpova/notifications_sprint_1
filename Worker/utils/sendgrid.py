from core.config import settings
from fastapi import Depends
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Email, Mail
import asyncio
import concurrent.futures


client: SendGridAPIClient = SendGridAPIClient(api_key=settings.sendgrid.api)


class SendGridEmailer:
    def __init__(
            self,
            client: SendGridAPIClient) -> None:
        self.client = client
        self.async_loop = asyncio.get_running_loop()

    async def mass_email(self, recievers: list[str], text: str,):
        from_email = settings.smtp.from_user
        mail = Mail(from_email=from_email, to_emails=recievers, subject=text)

        await self.async_loop.run_in_executor(
            None, self.client.send, (mail,))


emailer = SendGridEmailer(client=client)
