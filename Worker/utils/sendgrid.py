from core.config import settings
from fastapi import Depends
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Email, Mail


client: SendGridAPIClient = SendGridAPIClient(api_key=settings.sendgrid.api)


class SendGridEmailer:
    def __init__(
            self,
            client: SendGridAPIClient) -> None:
        self.client = client

    async def mass_email(self, recievers: list[str], text: str,):
        from_email = settings.smtp.from_user
        mail = Mail(from_email=from_email, to_emails=recievers, subject=text)
        self.client.send(message=mail)

emailer = SendGridEmailer(client=client)
