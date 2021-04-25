from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (check_existing_pos_staff, get_pos_staff,
                                 update_pos_staff)
from apps.merchant.validators import UpdatePosStaffMemberValidator

__all__ = ("UpdatePosStaffMember",)


class UpdatePosStaffMember(ServiceBase):
    def __init__(self, merchant, pos_staff, data):
        self.merchant = merchant
        self.pos_staff = pos_staff
        self.data = data

    def handle(self):
        data = self._validate_data()
        pos_staff = data["pos_staff"]
        pos_staff = update_pos_staff(
            pos_staff=pos_staff,
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            register_id=pos_staff.register.id,
            shift_start=pos_staff.shift_start,
            shift_end=pos_staff.shift_end,
        )

    def _validate_data(self):
        data = run_validator(UpdatePosStaffMemberValidator, self.data)
        email = data["email"]
        phone_number = data["phone_number"]
        pos_staff = self.pos_staff

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

        data["pos_staff"] = pos_staff
        return data
