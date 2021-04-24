import qrcode as qrcodelib
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.merchant.dbapi import get_pos_staff
from utils.shortcuts import img2base64

__all__ = ("GenerateLoginQrCodePosStaff",)


class GenerateLoginQrCodePosStaff(ServiceBase):
    def __init__(self, merchant, pos_staff_id):
        self.merchant = merchant
        self.pos_staff_id = pos_staff_id

    def handle(self):
        pos_staff = self._validate_data()
        login_token = pos_staff.get_login_token()
        image = qrcodelib.make(
            f"loqalposapp://auth/pos_session?access_token={login_token}"
        )
        return {"image_base64": img2base64(image)}

    def _validate_data(self):
        pos_staff = get_pos_staff(
            pos_staff_id=self.pos_staff_id, merchant_id=self.merchant.id
        )
        if not pos_staff:
            raise ValidationError(
                {"detail": ErrorDetail(_("Given POS staff is not valid."))}
            )
        return pos_staff
