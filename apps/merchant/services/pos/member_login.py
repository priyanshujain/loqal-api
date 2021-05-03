from datetime import timedelta

from django.utils.timezone import now
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_pos_session, get_active_pos_session,
                                 get_staff_from_username,
                                 expire_all_active_pos_session)
from apps.merchant.validators import (PosStaffAccessTokenValidator,
                                      PosStaffLoginValidator)
from apps.user.services.session import Session
from utils import auth

__all__ = (
    "ValidatePosStaffAccessToken",
    "PosStaffLogin",
    "PosStaffLogout",
)


class ValidatePosStaffAccessToken(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        data = self._validate_data()
        access_token = data["access_token"]
        username = data["username"]
        pos_staff = get_staff_from_username(username=username)
        if (
            (not pos_staff)
            or (pos_staff.login_token != access_token)
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
        return pos_staff

    def _validate_data(self):
        return run_validator(PosStaffAccessTokenValidator, self.data)


class PosStaffLogin(ServiceBase):
    def __init__(self, request, data):
        self.data = data
        self.request = request

    def handle(self):
        if self._check_already_loggedin():
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged in."))}
            )
        data = self._validate_data()
        access_token = data["access_token"]
        username = data["username"]
        pos_staff = get_staff_from_username(username=username)
        if (
            (not pos_staff)
            or (pos_staff.login_token != access_token)
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
                {"login_pin": [ErrorDetail(_("Login pin is incorrect."))]}
            )
        user = pos_staff.user
        auth.login(self.request, user)
        session = self.request.session
        # Assign the 4 hours expiration period
        if not session:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Session could not be created, please try again.")
                    )
                }
            )
        session.set_expiry(60 * 60 * 4)
        user_session = Session(request=self.request).create_session(user=user)
        return self._create_pos_session(
            staff_id=pos_staff.id, user_session_id=user_session.id
        )

    def _check_already_loggedin(self):
        user = self.request.user
        if user.is_authenticated:
            pos_session = get_active_pos_session(
                user_id=user.id,
                user_session_key=self.request.session.session_key,
            )
            if pos_session and pos_session.expires_at > now():
                return True
            else:
                auth.logout(self.request)
                if pos_session:
                    pos_session.expire()
        return False

    def _validate_data(self):
        return run_validator(PosStaffLoginValidator, self.data)

    def _create_pos_session(self, staff_id, user_session_id):
        pos_session = create_pos_session(
            staff_id=staff_id,
            user_session_id=user_session_id,
            expires_at=(now() + timedelta(hours=8)),
        )
        return pos_session


class PosStaffLogout(ServiceBase):
    pos_session = None

    def __init__(self, request):
        self.request = request

    def handle(self):
        if not self._check_already_loggedin():
            raise ValidationError(
                {"detail": ErrorDetail(_("You are already logged out."))}
            )
        auth.logout(self.request)
        if self.pos_session:
            self.pos_session.expire()

    def _check_already_loggedin(self):
        user = self.request.user
        if user.is_authenticated:
            pos_session = get_active_pos_session(
                user_id=user.id,
                user_session_key=self.request.session.session_key,
            )
            self.pos_session = pos_session
            if pos_session and pos_session.expires_at > now():
                return True
            else:
                auth.logout(self.request)
                if pos_session:
                    pos_session.expire()
                expire_all_active_pos_session(user_id=user.id)
        return False
