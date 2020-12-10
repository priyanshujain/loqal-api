from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import (get_account_member_by_id,
                               get_feature_access_role_by_id)
from apps.merchant.validators import (DisableMemberValidator,
                                    UpdateMemberRoleValidator)


__all__ = (
    "UpdateMemberRole",
    "DisableMember",
    "EnableMember",
)


class UpdateMemberRole(ServiceBase):
    def __init__(self, account_id, data):
        self.account_id = account_id
        self.data = data

    def _validate_data(self):
        data = run_validator(
            validator=UpdateMemberRoleValidator, data=self.data
        )

        role_id = data["role_id"]
        member_id = data["member_id"]
        role = get_feature_access_role_by_id(
            role_id=role_id, account_id=self.account_id
        )
        if not role:
            raise ValidationError(
                {"role_id": [ErrorDetail(_("Invalid role_id."))]}
            )

        account_member = get_account_member_by_id(
            member_id=member_id, account_id=self.account_id
        )
        if not account_member:
            raise ValidationError(
                {"account_member_id": [ErrorDetail(_("Invalid member_id."))]}
            )

        self.role = role
        self.account_member = account_member

    def execute(self):
        self._validate_data()

        account_member = self.account_member
        role = self.role
        account_member.update_role(role_id=role.id)


class MemberActivationBase(ServiceBase):
    def __init__(self, account_id, data):
        self.account_id = account_id
        self.data = data

    def _validate_data(self):
        data = run_validator(validator=DisableMemberValidator, data=self.data)

        member_id = data["member_id"]
        member = get_account_member_by_id(
            member_id=member_id, account_id=self.account_id
        )
        if not member:
            raise ValidationError(
                {"invite_id": [ErrorDetail(_("Invalid member_id."))]}
            )
        self.member = member

    def execute(self):
        self._validate_data()
        self.member.disable_member()


class DisableMember(MemberActivationBase):
    def execute(self):
        self._validate_data()
        self.member.disable_member()


class EnableMember(MemberActivationBase):
    def execute(self):
        self._validate_data()
        self.member.enable_member()
