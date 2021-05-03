from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (check_existing_pos_staff, get_pos_staff,
                                 update_pos_staff)
from apps.merchant.validators import UpdatePosStaffValidator
from apps.payment.dbapi import get_payment_qrcode_by_id

__all__ = ("UpdatePosStaff",)


class UpdatePosStaff(ServiceBase):
    def __init__(self, merchant, pos_staff_id, data):
        self.merchant = merchant
        self.pos_staff_id = pos_staff_id
        self.data = data

    def handle(self):
        data = self._validate_data()
        regsiter_qrcode = data["register_qrcode"]
        pos_staff = data["pos_staff"]
        pos_staff = update_pos_staff(
            pos_staff=pos_staff,
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            register_id=regsiter_qrcode.id,
            shift_start=data.get("shift_start", None),
            shift_end=data.get("shift_end", None),
        )

    def _validate_data(self):
        data = run_validator(UpdatePosStaffValidator, self.data)
        email = data["email"]
        phone_number = data["phone_number"]

        pos_staff = get_pos_staff(
            pos_staff_id=self.pos_staff_id, merchant_id=self.merchant.id
        )
        if not pos_staff:
            raise ValidationError(
                {"detail": ErrorDetail(_("Given POS staff is not valid."))}
            )

        existing_pos_staff = check_existing_pos_staff(
            email=email,
            phone_number=phone_number,
            merchant_id=self.merchant.id,
        )

        if existing_pos_staff and existing_pos_staff.id != pos_staff.id:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        "A staff already exists with provided email and phone number."
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

        data["pos_staff"] = pos_staff
        data["register_qrcode"] = qrcode
        return data
