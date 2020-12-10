from django.conf import settings
from django.template.loader import render_to_string

from utils.email import send_email_async

__all__ = ("SendAccountVerifyEmail",)


class SendAccountVerifyEmail:
    def __init__(self, user):
        self.user = user

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        token = user.email_verification_token
        key_path = f"/user/email-verification?key={token}"
        path = f"{settings.APP_BASE_URL}{key_path}"
        render_data = {"path": path}
        email_html = render_to_string("user_welcome_email.html", render_data)
        send_email_async((user.email), "Confirm your email", email_html)
