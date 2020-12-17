from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.banking.dbapi import get_bank_account
from apps.account.dbapi import get_consumer_account_by_phone_number, get_consumer_account_by_username
from apps.payment.validators import CreatePaymentRequestValidator
from apps.payment.dbapi import create_payment_request
from apps.provider.options import DEFAULT_CURRENCY


__all__ = ("CreatePaymentRequest", "ApprovePaymentRequest",)


class CreatePaymentRequest(ServiceBase):
    def __init__(self, account_id, data):
        self.data = data
        self.account_id = account_id

    def handle(self):
        payment_data = self._validate_data()
        payment_request = self._factory_payment_request(data=payment_data)
        return payment_request

    def _validate_data(self):
        data = run_validator(CreatePaymentRequestValidator, self.data)
        is_phone_number_based = data.get("is_phone_number_based")
        loqal_id = data.get("requested_to_loqal_id")
        phone_number = data.get("request_to_phone_number")

        if is_phone_number_based:
            consumer_account = get_consumer_account_by_phone_number(
                phone_number=phone_number
            )
        else:
            consumer_account = get_consumer_account_by_username(username=loqal_id)
        
        bank_account = get_bank_account(
            account_id=self.account_id
        )
        if not bank_account:
            raise ValidationError(
                {"detail": [ErrorDetail("Please add receiving bank account before creating payment request.")]}
            )
        data["requested_to_id"] = consumer_account.account.id
        return data
    
    def _factory_payment_request(self, data):
        return create_payment_request(
            account_id=self.account_id,
            requested_to_id=data["requested_to_id"],
            payment_amount=data["payment_amount"],
            tip_amount=data["tip_amount"],
            payment_currency=DEFAULT_CURRENCY,
        )



class ApprovePaymentRequest(ServiceBase):
    def __init__(self, account_id, data):
        self.data = data
        self.account_id = account_id

    def handle(self):
        payment_data = self._validate_data()

    def _validate_data(self):
        return self.data