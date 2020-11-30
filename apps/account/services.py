from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.account.dbapi import create_customer_account
from apps.user.dbapi import create_user_profile
from apps.user.models import User
from utils.email import send_email_async

__all__ = ("RegisterAccount",)


class RegisterAccount(ServiceBase):
    def __init__(
        self,
        first_name,
        last_name,
        email,
        company_name,
        country,
        contact_number,
        password,
    ):
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._company_name = company_name
        self._country = country
        self._contact_number = contact_number
        self._password = password

    def execute(self):
        self._validate_data()
        account = self._factory_account()
        user_profile = self._factory_user_profile()
        self._send_verfication_email(user=user_profile.user)

    def _validate_data(self):
        user_qs = User.objects.find_by_username(username=self._email)
        if user_qs.exists():
            raise ValidationError(
                {"email": [ErrorDetail(_("User email already exists."))]}
            )

    def _factory_account(self):
        return create_customer_account(
            company_name=self._company_name, country=self._country
        )

    def _factory_user_profile(self):
        return create_user_profile(
            first_name=self._first_name,
            last_name=self._last_name,
            email=self._email,
            contact_number=self._contact_number,
            password=self._password,
        )

    def _send_verfication_email(self, user):
        SendVerifyEmail(user=user).send()


class SendVerifyEmail:
    def __init__(self, user):
        self.user = user

    def send(self):
        self._send_email()

    def _send_email(self):
        user = self.user
        token = user.email_verification_token
        key_path = f"/user/email-verification?key={token}"
        path = f"{settings.APP_BASE_URL}{key_path}"
        render_data = {"path": path, "username": user.username}
        email_html = render_to_string("user_welcome_email.html", render_data)
        send_email_async((user.email), "Confirm your email", email_html)
