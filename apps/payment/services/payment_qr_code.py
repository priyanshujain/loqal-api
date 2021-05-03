from random import randint

from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import get_account_member_by_id
from apps.payment.dbapi import (assign_payment_qrcode, create_payment_qrcode,
                                get_cashier_qrcode, get_payment_qrcode,
                                get_payment_qrcode_by_id,
                                get_qrcode_by_register_name)
from apps.payment.models import qrcode
from apps.payment.validators import AssignPaymentQrCodeValidator

__all__ = (
    "CreateQrCode",
    "AssignQrCode",
    "UpdateQrCode",
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
            cashier_id=data.get("cashier_id"),
            register_name=data.get("register_name", ""),
        )

    def _validate_data(self):
        data = run_validator(AssignPaymentQrCodeValidator, self.data)
        cashier_id = data.get("cashier_id")
        register_name = data.get("register_name")

        if cashier_id:
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
            qr_code = get_cashier_qrcode(
                merchant_id=self.merchant_id, cashier_id=cashier_id
            )
            if qr_code:
                raise ValidationError(
                    {
                        "cashier_id": [
                            ErrorDetail(
                                _("This cashier already has a QR code.")
                            )
                        ]
                    }
                )
        if register_name:
            register_qr_code = get_qrcode_by_register_name(
                merchant_id=self.merchant_id, register_name=register_name
            )
            if register_qr_code:
                raise ValidationError(
                    {
                        "register_name": ErrorDetail(
                            _("A register already exists with this name.")
                        )
                    }
                )
        return data


class UpdateQrCode(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def handle(self):
        data = self._validate_data()
        assign_payment_qrcode(
            qrcode_id=data["qrcode_id"],
            merchant_id=self.merchant_id,
            cashier_id=data.get("cashier_id"),
            register_name=data.get("register_name", ""),
        )

    def _validate_data(self):
        data = run_validator(AssignPaymentQrCodeValidator, self.data)
        cashier_id = data.get("cashier_id")
        register_name = data.get("register_name")

        qr_code = get_payment_qrcode_by_id(
            qrcode_id=data.get("qrcode_id"), merchant_id=self.merchant_id
        )
        if not qr_code:
            raise ValidationError(
                {"detail": ErrorDetail(_("provided QR code is not valid."))}
            )

        if cashier_id:
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

        if register_name:
            register_qr_code = get_qrcode_by_register_name(
                merchant_id=self.merchant_id, register_name=register_name
            )

            if register_qr_code and register_qr_code.id != qr_code.id:
                raise ValidationError(
                    {
                        "register_name": ErrorDetail(
                            _("A register already exists with this name.")
                        )
                    }
                )
        return data
