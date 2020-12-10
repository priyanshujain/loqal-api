from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.account.dbapi import create_merchant_account
from apps.account.notifications import SendAccountVerifyEmail
from apps.merchant.dbapi import (create_account_member_on_reg,
                                 get_super_admin_role)
from apps.merchant.services import CreateDefaultRoles
from apps.user.dbapi import create_user, get_user_by_email

__all__ = ("CreateMerchantAccount",)


class CreateMerchantAccount(ServiceBase):
    def __init__(
        self,
        first_name,
        last_name,
        email,
        company_name,
        phone_number,
        password,
    ):
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._company_name = company_name
        self._contact_number = phone_number
        self._password = password

    def handle(self):
        self._validate_data()
        merchant_account = self._factory_merchant_account()
        user = self._factory_user()
        self._factory_default_roles(merchant_id=merchant_account.id)

        admin_role = get_super_admin_role(merchant_id=merchant_account.id)
        create_account_member_on_reg(
            user_id=user.id,
            merchant_id=merchant_account.id,
            member_role_id=admin_role.id,
        )
        self._send_verfication_email(user=user)

    def _validate_data(self):
        user = get_user_by_email(email=self._email)
        if user:
            raise ValidationError(
                {"email": [ErrorDetail(_("User email already exists."))]}
            )

    def _factory_merchant_account(self):
        return create_merchant_account(
            company_name=self._company_name, company_email=self._email
        )

    def _factory_user(self):
        return create_user(
            first_name=self._first_name,
            last_name=self._last_name,
            email=self._email,
            phone_number=self._contact_number,
            password=self._password,
        )

    def _factory_default_roles(self, merchant_id):
        service = CreateDefaultRoles(merchant_id=merchant_id)
        service.handle()

    def _send_verfication_email(self, user):
        SendAccountVerifyEmail(user=user).send()
