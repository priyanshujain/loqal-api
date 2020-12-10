from django.db.models.query_utils import InvalidQuery
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (create_account_member_from_team_invite,
                               get_member_invite_by_token)
from apps.merchant.validators import MemberSignupValidator

__all__ = ("MemberSignup",)


class MemberSignup(ServiceBase):
    def __init__(self, data):
        self.data = data

    def validate_data(self):
        data = run_validator(validator=MemberSignupValidator, data=self.data)

        invite_key = data["invite_key"]
        invite = get_member_invite_by_token(invite_key=invite_key)
        if not invite:
            raise ValidationError(
                {"invite_key": [ErrorDetail(_("Invalid invite_key."))]}
            )
        self.invite = invite
        self.data = data

    def handle(self):
        self.validate_data()

        invite = self.invite
        data = self.data
        first_name = data["first_name"]
        last_name = data["last_name"]
        position = data["position"]
        phone_number = data["phone_number"]
        password = data["password"]

        create_account_member_from_team_invite(
            invite=invite,
            first_name=first_name,
            last_name=last_name,
            position=position,
            phone_number=phone_number,
            password=password,
        )
        invite.expire_code()
