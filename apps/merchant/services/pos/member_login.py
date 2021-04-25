from utils import auth
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import get_staff_from_access_token
from apps.merchant.validators import (
    PosStaffAccessTokenValidator,
    PosStaffLoginValidator,
)

__all__ = ("ValidatePosStaffAccessToken",)


class ValidatePosStaffAccessToken(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        data = self._validate_data()
        access_token = data["access_token"]
        pos_staff = get_staff_from_access_token(access_token=access_token)
        if (
            (not pos_staff)
            or (not pos_staff.account_active)
            or (pos_staff.user.is_disabled)
        ):
            raise ValidationError(
                {
                    "access_token": ErrorDetail(
                        _(
                            "Login QR code is invalid."
                            " Please contact the store owner and try again"
                        )
                    )
                }
            )
        return True

    def _validate_data(self):
        return run_validator(PosStaffAccessTokenValidator, self.data)


class PosStaffLogin(ServiceBase):
    def __init__(self, request, data):
        self.data = data
        self.request = request

    def handle(self):
        data = self._validate_data()
        access_token = data["access_token"]
        pos_staff = get_staff_from_access_token(access_token=access_token)
        if (
            (not pos_staff)
            or (not pos_staff.account_active)
            or (pos_staff.user.is_disabled)
        ):
            raise ValidationError(
                {
                    "access_token": ErrorDetail(
                        _(
                            "Login QR code is invalid."
                            " Please contact the store owner and try again"
                        )
                    )
                }
            )
        login_pin = data["login_pin"]
        if login_pin != pos_staff.login_pin:
            raise ValidationError(
                {"login_in": ErrorDetail(_("Login pin is incorrect."))}
            )
        user = pos_staff.user
        auth.login(self.request, user)

    def _validate_data(self):
        return run_validator(PosStaffAccessTokenValidator, self.data)
