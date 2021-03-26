from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from utils.sms import send_sms

__all__ = ("InviteConsumerBySMS",)


class InviteConsumerBySMS(ServiceBase):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def handle(self):
        text = _(
            f"Thanks for joining Loqal. Please click the link(loqal.app.link) to download the app."
            "\n\n Thanks\nTeam Loqal"
        )
        try:
            is_success = send_sms(body=text, phone_number=self.phone_number)
            if not is_success:
                raise ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("Something went wrong. Please try again later.")
                        )
                    }
                )
            return True
        except Exception:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Phone number is not valid. Please "
                            "correct the phone number and try again."
                        )
                    )
                }
            )
