from random import randint

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.payment.dbapi import create_payment_qrcode, get_payment_qrcode

__all__ = ("CreatePayment",)


class CreatePayment(ServiceBase):
    def __init__(self, account_id, data):
        self.data = data
        self.account_id = account_id

    def handle(self):
        payment_data = self._validate_data()
        merchant_account = payment_data["merchant_account"]
        payment_amount = payment_data["payment_amount"]
        tip_amount = payment_data["tip_amount"]
        payment_currency = payment_data["payment_currency"]

        sender_bank_account = get_bank_account(account_id=self.account_id)

        if not sender_bank_account:
            raise ValidationError(
                {"detail": ErrorDetail("Please add the bank account before making payment.")}
            )



class GenerateUsername(object):
    def __init__(self, user):
        self.user = user
    
    def generate(self):
        return randint(111111, 999999)

    def handle(self):
        qrcode_id = self.generate()
        while get_payment_qrcode(qrcode_id=qrcode_id):
                   qrcode_id = self.generate()
        return qrcode_id