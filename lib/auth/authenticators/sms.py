from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from utils.decorators import classproperty
from utils.otp import TOTP
from utils.sms import send_sms, sms_available

from .base import ActivationMessageResult, AuthenticatorInterface, OtpMixin


class SmsInterface(OtpMixin, AuthenticatorInterface):
    """This interface sends OTP codes via text messages to the user."""

    type = 2
    interface_id = "sms"
    name = _("Text Message")
    description = _(
        "This authenticator sends you text messages for "
        "verification.  It's useful as a backup method "
        "or when you do not have a phone that supports "
        "an authenticator application."
    )
    code_ttl = 120

    @classproperty
    def is_available(cls):
        return sms_available()

    def generate_new_config(self):
        config = super(SmsInterface, self).generate_new_config()
        config["phone_number"] = None
        return config

    def make_otp(self):
        return TOTP(
            self.config["secret"],
            digits=6,
            interval=self.code_ttl,
            default_window=1,
        )

    def _get_phone_number(self):
        return self.config["phone_number"]

    def _set_phone_number(self, value):
        self.config["phone_number"] = value

    def _get_phone_number_country(self):
        return self.config["phone_number_country"]

    def _set_phone_number_country(self, value):
        self.config["phone_number_country"] = value

    phone_number = property(_get_phone_number, _set_phone_number)
    del _get_phone_number, _set_phone_number

    phone_number_country = property(
        _get_phone_number_country, _set_phone_number_country
    )
    del _get_phone_number_country, _set_phone_number_country

    def activate(self, request):
        phone_number = self.config["phone_number"]
        if len(phone_number) == 10:
            mask = "(***) ***-**%s" % (phone_number[-2:])
        else:
            mask = "%s%s" % ((len(phone_number) - 2) * "*", phone_number[-2:])

        if self.send_text(request=request):
            return ActivationMessageResult(
                _(
                    "A confirmation code was sent to %(phone_mask)s. "
                    "It is valid for %(ttl)d seconds."
                )
                % {
                    "phone_mask": "<strong>%s</strong>" % mask,
                    "ttl": self.code_ttl,
                }
            )
        return ActivationMessageResult(
            _(
                "Error: we failed to send a text message to you. You "
                "can try again later or sign in with a different method."
            ),
            type="error",
        )

    def send_text(self, for_enrollment=False, request=None):
        ctx = {"code": self.make_otp().generate_otp()}

        if for_enrollment:
            text = _("%(code)s is your Loqal phone number enrollment code. ")
        else:
            text = _("%(code)s is your Loqal authentication code.")

        if request is not None:
            text = u"%s\n\n%s" % (text, _("Requested from %(ip)s"))
            ctx["ip"] = request.ip

        return send_sms(
            text % ctx,
            phone_number=self.phone_number,
            phone_number_country=self.phone_number_country,
        )
