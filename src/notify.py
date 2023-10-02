import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, To, Content, Mail
from sendgrid.helpers.mail.exceptions import SendGridException

load_dotenv()


def send_mail(message: str) -> None:
    sg_client = SendGridAPIClient()
    from_address = Email(os.environ["FROM_ADDRESS"])
    to_address = To(os.environ["TO_ADDRESS"])
    content = Content("text/html", message)
    mail = Mail(from_address, to_address, "New Stock Data", content)
    response = sg_client.client.mail.send.post(request_body=mail.get())
    if response.status_code != 202:
        raise SendGridException("Error sending email notification")
    return
