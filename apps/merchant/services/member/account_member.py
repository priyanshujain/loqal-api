from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.constants import DEFAULT_ROLE
from apps.merchant.dbapi import get_account_member_by_id, update_member_role
from apps.merchant.validators import (DisableMemberValidator,
                                      UpdateMemberRoleValidator)

__all__ = (
    "UpdateMemberRole",
    "DisableMember",
    "EnableMember",
)


class UpdateMemberRole(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def _validate_data(self):
        data = run_validator(
            validator=UpdateMemberRoleValidator, data=self.data
        )
        member_id = data["member_id"]
        account_member = get_account_member_by_id(
            member_id=member_id, merchant_id=self.merchant_id
        )
        if not account_member:
            raise ValidationError(
                {"account_member_id": [ErrorDetail(_("Invalid member_id."))]}
            )
        self.account_member = account_member
        return data

    def handle(self):
        data = self._validate_data()
        account_member = self.account_member
        role = data["role"]
        update_member_role(role_id=account_member.role.id, data=role)


class MemberActivationBase(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def _validate_data(self):
        data = run_validator(validator=DisableMemberValidator, data=self.data)

        member_id = data["member_id"]
        member = get_account_member_by_id(
            member_id=member_id, merchant_id=self.merchant_id
        )
        if not member:
            raise ValidationError(
                {"invite_id": [ErrorDetail(_("Invalid member_id."))]}
            )
        self.member = member

    def handle(self):
        self._validate_data()
        self.member.disable_member()


class DisableMember(MemberActivationBase):
    def handle(self):
        self._validate_data()
        self.member.disable_member()


class EnableMember(MemberActivationBase):
    def handle(self):
        self._validate_data()
        self.member.enable_member()
