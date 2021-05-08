import re
from random import randint

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.account.dbapi import (check_account_username,
                                create_consumer_account,
                                get_merchant_account_by_email)
from apps.account.notifications import SendConsumerAccountVerifyEmail
from apps.account.validators import CreateConsumerAccountValidator
from apps.payment.dbapi import create_payment_register
from apps.user.dbapi import create_user, get_consumer_user_by_email
from apps.user.options import CustomerTypes

from .accept_consumer_terms import AcceptTerms

__all__ = (
    "CreateConsumerAccount",
    "GenerateUsername",
)


class CreateConsumerAccount(ServiceBase):
    def __init__(self, request, data):
        self.data = data
        self.request = request

    def handle(self):
        data = self._validate_data()
        user = self._factory_user()
        consumer_account = self._factory_account(user=user)
        self._create_pending_payment_request(consumer_account=consumer_account)
        AcceptTerms(
            request=self.request,
            account=consumer_account.account,
            user=user,
            data={
                "consent_timestamp": data["consent_timestamp"],
                "payment_terms_url": data["payment_terms_url"],
            },
        ).handle()
        self._send_verfication_email(user=user)

        return consumer_account

    def _validate_data(self):
        data = run_validator(
            validator=CreateConsumerAccountValidator, data=self.data
        )
        self._first_name = data["first_name"]
        self._last_name = data["last_name"]
        self._email = data["email"]
        self._password = data["password"]

        user = get_consumer_user_by_email(email=self._email)
        if user:
            raise ValidationError(
                {
                    "email": [
                        ErrorDetail(
                            _("A user with this email already exists.")
                        )
                    ]
                }
            )

        user = get_merchant_account_by_email(email=self._email)
        if user:
            raise ValidationError(
                {
                    "detail": [
                        ErrorDetail(
                            _(
                                "You already signed for a "
                                "Loqal merchant account with this email. "
                                "Please use a different email."
                            )
                        )
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
            customer_type=CustomerTypes.CONSUMER,
        )

    def _send_verfication_email(self, user):
        SendConsumerAccountVerifyEmail(user=user).send()


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
