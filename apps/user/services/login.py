from django.contrib import auth
from utils import auth as custom_auth
from django.utils.translation import gettext as _
from otpauth import OtpAuth

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.user.dbapi import create_session
from apps.user.notifications import SendLoginAlert
from apps.user.validators import UserLoginValidator

__all__ = ("Login",)


class Login(ServiceBase):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def _validate_data(self, data):
        data = run_validator(validator=UserLoginValidator, data=data)

    def execute(self):
        data = self.data
        self._validate_data(data=data)
        user = auth.authenticate(
            username=data["email"], password=data["password"]
        )

        if user:
            if user.is_disabled:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("Your account has been disabled.")
                        )
                    }
                )

            if not user.two_factor_auth:
                return self._auth_login(user)

            if user.two_factor_auth and "tfa_code" not in data:
                raise ValidationError(
                    {"tfa_code": [ErrorDetail(_("This is required."))]}
                )

            if OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                return self._auth_login(user)
            else:
                raise ValidationError(
                    {
                        "tfa_code": [
                            ErrorDetail(
                                _("Invalid two factor authentication code.")
                            )
                        ]
                    }
                )
        else:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid username or password."))}
            )

    def _auth_login(self, user):
        request = self.request
        custom_auth.login(request, user)
        self._factory_session(user=user)
        service = SendLoginAlert(user=user, session=request.session)
        service.send()

    def _factory_session(self, user):
        # TODO: Combine cache based session and models based session so that
        #       we have a record of expired sessions.
        data = self.data
        session = self.request.session
        ifconfig = data["ifconfig"]

        # from cache based session
        user_agent = session["user_agent"]
        ip_address = session["ip"]
        is_ip_routable = session["is_ip_routable"]
        last_activity = session["last_activity"]
        ip_country_iso = session["cf_ip_country"]

        # from maxmind ifconfig
        country_iso = ifconfig.get("country_iso", "")
        region = ifconfig.get("region", "")
        region_code = ifconfig.get("region_code", "")
        latitude = ifconfig.get("latitude", "")
        longitude = ifconfig.get("longitude", "")
        timezone = ifconfig.get("timezone", "")
        asn = ifconfig.get("asn_org", "")
        asn_code = ifconfig.get("asn", "")

        create_session(
            user_id=user.id,
            session_key=session.session_key,
            user_agent=user_agent,
            ip_address=ip_address,
            is_ip_routable=is_ip_routable,
            last_activity=last_activity,
            ip_country_iso=ip_country_iso,
            country_iso=country_iso,
            region=region,
            region_code=region_code,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            asn=asn,
            asn_code=asn_code,
        )
