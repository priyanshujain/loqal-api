from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.merchant.dbapi import get_pos_staff

__all__ = ("GeneratePinPosStaff",)


class GeneratePinPosStaff(ServiceBase):
    def __init__(self, merchant, pos_staff_id):
        self.merchant = merchant
        self.pos_staff_id = pos_staff_id

    def handle(self):
        pos_staff = self._validate_data()
        login_pin = pos_staff.generate_pin(
            merchant_id=self.merchant.id, save=True
        )
        return login_pin

    def _validate_data(self):
        pos_staff = get_pos_staff(
            pos_staff_id=self.pos_staff_id, merchant_id=self.merchant.id
        )
        if not pos_staff:
            raise ValidationError(
                {"detail": ErrorDetail(_("Given POS staff is not valid."))}
            )
        return pos_staff
