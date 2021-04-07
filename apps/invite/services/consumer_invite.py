from re import I

from django.db import reset_queries
from django.utils.translation import gettext as _
from phonenumbers import phonenumber

from api.exceptions import ErrorDetail, ValidationError
from api.services import ServiceBase
from apps.invite.dbapi import create_c2c_invite, get_c2c_invite
from apps.user.dbapi import get_user_by_phone
from apps.user.options import CustomerTypes
from utils.sms import send_sms

__all__ = ("InviteConsumer",)


class InviteConsumer(ServiceBase):
    def __init__(self, phone_number, consumer, resend=False):
        self.phone_number = phone_number
        self.consumer = consumer
        self.resend = resend

    def handle(self):
        consumer = self.consumer
        invite_user = get_user_by_phone(
            phone_number=self.phone_number,
            customer_type=CustomerTypes.CONSUMER,
        )
        if invite_user:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "A user already exists with this phone number on Loqal App."
                        )
                    )
                }
            )

        c2c_invite = get_c2c_invite(
            phone_number=self.phone_number, consumer_id=consumer.id
        )
        if not self.resend and c2c_invite:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "You have already invited a person with this phone number."
                        )
                    )
                }
            )

        consumer_name = f"{consumer.user.first_name} {consumer.user.last_name}"
        text = _(
            f"You are invite to Loqal by {consumer_name}. "
            "Please click the link(loqal.app.link) to download the app."
            "\n\n Thanks\nTeam Loqal"
        )

        if not self.resend:
            c2c_invite = create_c2c_invite(
                phone_number=self.phone_number, consumer_id=consumer.id
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
        return c2c_invite
