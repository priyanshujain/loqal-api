from django.template.loader import render_to_string

from utils.email import send_email_async


class SendVerifyMicroDepositEmail(object):
    def __init__(self, email):
        self.email = email

    def send(self):
        self._send_email()

    def _send_email(self):
        email_html = render_to_string("verify_micro_deposit.html", {})
        send_email_async(
            (self.email),
            "Verify your bank account",
            email_html,
        )
