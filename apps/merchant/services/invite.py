from django.utils.translation import gettext as _
from rest_framework.utils.field_mapping import get_field_kwargs

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.account.dbapi import get_consumer_account_by_phone_number
from utils.sms import send_sms

__all__ = ("InviteConsumerBySMS",)


class InviteConsumerBySMS(ServiceBase):
    def __init__(self, merchant, phone_number, request_payment=False):
        self.phone_number = phone_number
        self.merchant = merchant
        self.request_payment = request_payment

    def handle(self):
        consumer = get_consumer_account_by_phone_number(
            phone_number=self.phone_number
        )
        if consumer:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("The user already exists on Loqal App.")
                    )
                }
            )

        text = _(
            f"{self.merchant.profile.full_name} has invited you to "
            "the Loqal App. Please click the link(loqal.app.link) to register and "
            "make secure payments. \n\n Thanks\nTeam Loqal"
        )
        if self.request_payment:
            text = _(
                f"{self.merchant.profile.full_name} requested a secure "
                "payment from you via Loqal. "
                "Our records indicate you do not have a Loqal account yet. "
                "Please click the link(loqal.app.link) to register and "
                "make payment. \n\n Thanks\nTeam Loqal"
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
