from random import randint

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import get_account_member_by_id
from apps.payment.dbapi import (assign_payment_qrcode, create_payment_qrcode,
                                get_payment_qrcode)
from apps.payment.validators import AssignPaymentQrCodeValidator

__all__ = (
    "CreateQrCode",
    "AssignQrCode",
)


class CreateQrCode(ServiceBase):
    def __init__(self):
        pass

    def generate_random_id(self):
        return randint(111111, 999999)

    def generate_unique_id(self):
        qrcode_id = self.generate_random_id()
        while get_payment_qrcode(qrcode_id=qrcode_id):
            qrcode_id = self.generate_unique_id()
        return qrcode_id

    def handle(self):
        qrcode_id = self.generate_unique_id()
        return create_payment_qrcode(qrcode_id=qrcode_id)


class AssignQrCode(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def handle(self):
        data = self._validate_data()
        assign_payment_qrcode(
            qrcode_id=data["qrcode_id"],
            merchant_id=self.merchant_id,
            cashier_id=data["cashier_id"],
        )

    def _validate_data(self):
        data = run_validator(AssignPaymentQrCodeValidator, self.data)
        cashier_id = data["cashier_id"]

        merchant_member = get_account_member_by_id(
            member_id=cashier_id, merchant_id=self.merchant_id
        )
        if not merchant_member:
            raise ValidationError(
                {
                    "cashier_id": [
                        ErrorDetail(
                            _("Cashier does not belong to the merchant.")
                        )
                    ]
                }
            )
        return data
