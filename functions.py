from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from django.conf import settings
from django.core.mail import send_mail as send_mail_


def send_mail(to_emails, content, subject):
    """
    sends emails using settings.EMAIL_HOST_USER
    :param to_emails: emails to which the email is to be sent
    :param content: content of the email
    :param subject: subject of the email
    :return:
    """
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    send_mail_(
        subject=subject,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=to_emails,
        message="",
        html_message=content,
    )
