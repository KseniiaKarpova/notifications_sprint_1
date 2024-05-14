import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, BaseLoader
from services import BaseService
from models.messages import Email
from core.config import settings


server: smtplib.SMTP = None

def get_server():
    return server


class EmailService(BaseService):

    def rendering_template(self, template, data) -> str:
        env = Environment(loader=BaseLoader())
        env.from_string(template)
        output = template.render(**data)
        return output

    def send(self, email: Email):
        message = EmailMessage()

        message['To'] = ",".join([email.To])
        message['Subject'] = email.Subject

        message.add_alternative(email.Message, subtype='html')

        try:
            get_server().sendmail(settings.smpt.FROM, email.To, message.as_string())
        except smtplib.SMTPException as exc:
            return False
        else:
            return message.as_string()

def get_email_services():
    return EmailService