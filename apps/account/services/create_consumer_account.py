from datetime import date
from io import SEEK_CUR

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import create_consumer_account
from apps.account.notifications import SendVerifyEmail
from apps.account.validators import CreateConsumerAccountValidator
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.provider.lib.api import account
from apps.user.dbapi import create_user, get_user_by_email

__all__ = ("CreateConsumerAccount",)


class CreateConsumerAccount(ServiceBase):
    def __init__(self, data, ip_address):
        self.data = data
        self.ip_address = ip_address

    def execute(self):
        self._validate_data()
        user = self._factory_user()
        consumer_account = self._factory_account(user=user)
        self._send_verfication_email(user=user)
        self._create_dwolla_account(consumer_account=consumer_account)

    def _validate_data(self):
        data = run_validator(
            validator=CreateConsumerAccountValidator, data=self.data
        )
        self._first_name = data["first_name"]
        self._last_name = data["last_name"]
        self._email = data["email"]
        self._password = data["password"]

        user = get_user_by_email(email=self._email)
        if user:
            raise ValidationError(
                {
                    "email": [
                        ErrorDetail(_("User with this email already exists."))
                    ]
                }
            )

    def _factory_account(self, user):
        # TODO: Store spotlight terms and condition consent record
        return create_consumer_account(user_id=user.id)

    def _factory_user(self):
        return create_user(
            first_name=self._first_name,
            last_name=self._last_name,
            email=self._email,
            password=self._password,
        )

    def _create_dwolla_account(self, consumer_account):
        user = consumer_account.user
        account = consumer_account.account
        psp_req_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "ip_address": self.ip_address,
        }
        psp_action = CreateConsumerAccountAPIAction(data=psp_req_data)
        response = psp_action.create()
        dwolla_customer_id = response["dwolla_customer_id"]
        account.add_dwolla_id(dwolla_id=dwolla_customer_id)

    def _send_verfication_email(self, user):
        SendVerifyEmail(user=user).send()


class CreateConsumerAccountAPIAction(ProviderAPIActionBase):
    def create(self, data):
        response = self.client.account.create_consumer_account(data=data)
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "Banking service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
            "dwolla_customer_id": response["data"]["dwolla_customer_id"],
        }
