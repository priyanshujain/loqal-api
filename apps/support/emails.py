from django.conf import settings
from django.template.loader import render_to_string

from utils.email import send_email_async

__all__ = ("SendAccountVerifyEmail",)


class SendSupportEmail(object):
    def __init__(self, user, message, issue_tracking_id):
        self.user_email = user.email
        self.user_name = user.first_name
        self.message = message
        self.issue_tracking_id = issue_tracking_id

    def send(self):
        self._send_email()

    def _send_email(self):
        render_data = {"name": self.user_name, "message": self.message}
        email_html = render_to_string("support_email.html", render_data)
        send_email_async(
            (
                self.user_email,
                settings.SPOTLIGHT_ADMIN_EMAIL,
            ),
            f"Support request #{self.issue_tracking_id}",
            email_html,
        )
