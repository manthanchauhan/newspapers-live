from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from django.conf import settings


def send_mail(to_emails, content, subject):
    """
    sends emails using settings.EMAIL_HOST_USER
    :param to_emails: emails to which the email is to be sent
    :param content: content of the email
    :param subject: subject of the email
    :return:
    """
    # create sendgrid client
    sg = SendGridAPIClient(config('SEND_GRID_API_KEY'))

    # create a Mail object to send
    email = Mail(from_email=settings.EMAIL_HOST_USER, to_emails=to_emails, subject=subject,
                 html_content=content)

    # send email and catch the response
    response = sg.send(message=email)

    # send status
    return response == 202

