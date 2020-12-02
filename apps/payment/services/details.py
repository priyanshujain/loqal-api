from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.payment.dbapi import get_payment_request, get_transaction


class PaymentDetails(ServiceBase):
    def __init__(self, account_id, payment_request_id):
        self.payment_request_id = payment_request_id
        self.account_id = account_id

    def execute(self):
        payment_request = self._get_payment_request()
        return payment_request

    def _get_payment_request(self):
        payment_request = get_payment_request(
            payment_request_id=self.payment_request_id,
            account_id=self.account_id,
        )

        return payment_request


class TransactionDetails(ServiceBase):
    def __init__(self, account_id, transaction_id):
        self.transaction_id = transaction_id
        self.account_id = account_id

    def execute(self):
        transaction = self._get_transaction()
        return transaction

    def _get_transaction(self):
        transaction = get_transaction(
            transaction_id=self.transaction_id, account_id=self.account_id,
        )

        return transaction
