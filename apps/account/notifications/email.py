from django.conf import settings
from django.template.loader import render_to_string
from sendgrid.helpers.mail import file_name

from utils.email import send_email_async

__all__ = (
    "SendConsumerAccountVerifyEmail",
    "SendMerchantAccountVerifyEmail",
    "SendConsumerTermsEmail",
)


class SendConsumerAccountVerifyEmail(object):
    def __init__(self, user):
        self.user = user

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        token = user.email_verification_token
        key_path = f"/email-verification?key={token}"
        path = f"{settings.CONSUMER_APP_WEB_BASE_URL}{key_path}"
        render_data = {"path": path}
        email_html = render_to_string(
            "consumer_email_verification.html", render_data
        )
        send_email_async((user.email), "Confirm your email", email_html)


class SendConsumerTermsEmail(object):
    def __init__(self, user, file_path):
        self.user = user
        self.file_path = file_path

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        render_data = {}
        email_html = render_to_string(
            "consumer_terms_consent.html", render_data
        )
        send_email_async(
            to_emails=(user.email),
            subject="Accepted Terms of Service and Privacy Policy",
            content=email_html,
            file_path=self.file_path,
            file_name="payment_terms.pdf",
        )


class SendMerchantAccountVerifyEmail(object):
    def __init__(self, user):
        self.user = user

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        token = user.email_verification_token
        key_path = f"/user/email-verification?key={token}"
        path = f"{settings.MERCHANT_APP_WEB_BASE_URL}{key_path}"
        render_data = {"path": path}
        email_html = render_to_string(
            "merchant_email_verification.html", render_data
        )
        send_email_async((user.email), "Confirm your email", email_html)
