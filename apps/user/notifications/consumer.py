from django.conf import settings
from django.template.loader import render_to_string
from user_agents import parse

from utils.email import send_email_async

__all__ = (
    "SendLoginAlert",
    "SendPasswordChangeAlert",
    "SendResetPasswordEmail",
)


class SessionData:
    def __init__(self, session):
        self.session = session

    @property
    def data(self):
        return self._get_session_data()

    def _get_session_data(self):
        user_agent = parse(self.session["user_agent"])
        browser = user_agent.browser.family
        os_family = user_agent.os.family
        os_version = user_agent.os.version_string
        os_full_name = f"{os_family} {os_version}"
        ip = self.session["ip"]
        last_activity = self.session["last_activity"]

        return {
            "ip": ip,
            "os_name": os_full_name,
            "browser": browser,
            "last_activity": last_activity.strftime(
                "%X %p (%Z) %A, %b %d, %Y"
            ),
        }


class SendLoginAlert(object):
    def __init__(self, user, session):
        self.user = user
        self.session = session

    def send(self):
        session_data = SessionData(session=self.session).data
        SendLoginAlertEmail(user=self.user, session_data=session_data).send()


class SendLoginAlertEmail:
    def __init__(self, user, session_data):
        self.user = user
        self.session_data = session_data

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        render_data = dict(**self.session_data, email=user.email)
        email_html = render_to_string("login_alert.html", render_data)
        send_email_async((user.email), "Spotlight log in alert", email_html)


class SendPasswordChangeAlert(object):
    def __init__(self, user, session):
        self.user = user
        self.session = session

    def send(self):
        session_data = SessionData(session=self.session).data
        SendPasswordChangeAlertEmail(
            user=self.user, session_data=session_data
        ).send()


class SendPasswordChangeAlertEmail:
    def __init__(self, user, session_data):
        self.user = user
        self.session_data = session_data

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        render_data = dict(**self.session_data, email=user.email)
        email_html = render_to_string(
            "password_change_alert.html", render_data
        )
        send_email_async(
            (user.email), "Spotlight password change alert", email_html
        )


class SendResetPasswordEmail:
    def __init__(self, reset_password_object):
        self.user = reset_password_object.user
        self.token = reset_password_object.token

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        token = self.token

        render_data = {
            "website_name": settings.APP_BASE_URL,
            "path": f"{settings.APP_BASE_URL}/user/forgot/key/{token}",
        }
        email_html = render_to_string("reset_password_email.html", render_data)
        send_email_async((user.email), "Reset your password", email_html)
