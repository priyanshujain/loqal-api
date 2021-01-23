from random import randint

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import check_account_username, create_consumer_account
from apps.account.notifications import SendConsumerAccountVerifyEmail
from apps.account.validators import CreateConsumerAccountValidator
from apps.payment.dbapi import create_payment_register
from apps.provider.lib.actions import ProviderAPIActionBase
from apps.user.dbapi import create_user, get_user_by_email

__all__ = (
    "CreateConsumerAccount",
    "GenerateUsername",
)


class CreateConsumerAccount(ServiceBase):
    def __init__(self, data, ip_address):
        self.data = data
        self.ip_address = ip_address

    def handle(self):
        data = self._validate_data()
        user = self._factory_user()
        consumer_account = self._factory_account(user=user)
        self._send_verfication_email(user=user)
        self._create_dwolla_account(consumer_account=consumer_account)
        return consumer_account

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
        return data

    def _factory_account(self, user):
        # TODO: Store spotlight terms and condition consent record
        username = GenerateUsername(user=user).handle()
        consumer_account = create_consumer_account(
            user_id=user.id, username=username
        )
        self._factory_payment_register(account_id=consumer_account.account.id)
        return consumer_account

    def _factory_payment_register(self, account_id):
        create_payment_register(account_id=account_id)

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
        psp_action = CreateConsumerAccountAPIAction(account_id=account.id)
        response = psp_action.create(data=psp_req_data)
        dwolla_customer_id = response["dwolla_customer_id"]
        status = response["status"]
        verification_status = response["verification_status"]
        account.add_dwolla_id(dwolla_id=dwolla_customer_id, save=False)
        account.update_status(
            status=status, verification_status=verification_status
        )

    def _send_verfication_email(self, user):
        SendConsumerAccountVerifyEmail(user=user).send()


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
            "verification_status": response["data"].get("verification_status"),
            "dwolla_customer_id": response["data"]["dwolla_customer_id"],
        }


class GenerateUsername(object):
    def __init__(self, user):
        self.user = user

    def generate(self):
        number = randint(11111, 99999)
        first_name_i = self.user.first_name[0].lower()
        last_name_i = self.user.last_name[0].lower()
        return f"{number}@{first_name_i}{last_name_i}"

    def handle(self):
        username = self.generate()
        while check_account_username(username=username):
            username = self.generate()
        return username
