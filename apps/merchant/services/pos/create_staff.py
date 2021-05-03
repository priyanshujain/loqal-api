from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (check_staff_exists, create_pos_staff,
                                 get_merchant_user)
from apps.merchant.validators import CreatePosStaffValidator
from apps.payment.dbapi import get_payment_qrcode_by_id

__all__ = ("CreatePosStaff",)


class CreatePosStaff(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self._validate_data()
        regsiter_qrcode = data["register_qrcode"]
        pos_staff = create_pos_staff(
            merchant_id=self.merchant.id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            register_id=regsiter_qrcode.id,
            shift_start=data.get("shift_start", None),
            shift_end=data.get("shift_end", None),
        )
        return pos_staff

    def _validate_data(self):
        data = run_validator(CreatePosStaffValidator, self.data)
        email = data["email"]
        phone_number = data["phone_number"]

        user = get_merchant_user(email=email, phone_number=phone_number)
        if user:
            if check_staff_exists(
                merchant_id=self.merchant.id, user_id=user.id
            ):
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _(
                                "A staff with this email and phone number already exists."
                            )
                        )
                    }
                )
            else:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _(
                                "A staff with this email and phone number already exists with another merchant."
                            )
                        )
                    }
                )

        register_id = data["register_id"]

        qrcode = get_payment_qrcode_by_id(
            qrcode_id=register_id, merchant_id=self.merchant.id
        )
        if not qrcode:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Provided register qrcode is not valid.")
                    )
                }
            )

        data["register_qrcode"] = qrcode
        return data
