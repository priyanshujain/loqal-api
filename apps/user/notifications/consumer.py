from django.conf import settings
from django.template.loader import render_to_string

from utils.email import send_email_async

__all__ = ("SendConsumerResetPasswordEmail",)


class SendConsumerResetPasswordEmail(object):
    def __init__(self, reset_password_object):
        self.user = reset_password_object.user
        self.token = reset_password_object.token

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        token = self.token

        render_data = {
            "website_name": settings.CONSUMER_APP_WEB_BASE_URL,
            "path": f"{settings.CONSUMER_APP_WEB_BASE_URL}/reset-password?key={token}",
        }
        email_html = render_to_string(
            "consumer_reset_password.html", render_data
        )
        send_email_async(
            (user.email), "Reset your loqal app password", email_html
        )
