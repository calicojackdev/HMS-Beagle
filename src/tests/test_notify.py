from unittest import TestCase

from sendgrid.helpers.mail.exceptions import SendGridException

from src.notify import send_mail


class TestSendMail(TestCase):
    def setUp(self):
        self.message = "This is a test from TestSendMail"

    def test_send_mail(self):
        try:
            send_mail(self.message)
        except SendGridException as sge:
            assert self.fail(sge)
        except Exception as error:
            assert self.fail(error)
