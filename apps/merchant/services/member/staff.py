from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.member.dbapi import (add_account_access_to_profile,
                               create_admin_account_access,
                               get_account_member_by_profile,
                               get_active_account_access_by_account,
                               get_active_account_access_by_profile,
                               get_admin_account_access_by_id,
                               get_standard_user_role)
from apps.member.validators import (AddAccountAccessSerializer,
                                    RemoveAccountAccessSerializer)

__all__ = (
    "AddAdminMemberAccountAccess",
    "RemoveAdminMemberAccountAccess",
)


class AddAdminMemberAccountAccess(ServiceBase):
    def __init__(self, data):
        self.data = data

    def execute(self):
        self.data = self._validate_data()
        return self._factory_account_access()

    def _validate_data(self):
        data = run_validator(AddAccountAccessSerializer, self.data)

        account_member = get_account_member_by_profile(
            profile_id=data["profile_id"]
        )
        if not account_member:
            raise ValidationError(
                {"detail": ErrorDetail(_("Account member does not exist."))}
            )

        if not account_member.profile.user.is_admin_role():
            raise ValidationError(
                {"detail": ErrorDetail(_("Profile user is not admin."))}
            )

        account_access = get_active_account_access_by_account(
            account_id=data["account_id"]
        )

        if account_access:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Admin account access already exists.")
                    )
                }
            )

        account_access = get_active_account_access_by_profile(
            profile_id=data["profile_id"]
        )

        if account_access:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("User already have access to another account.")
                    )
                }
            )

        standard_user_role = get_standard_user_role(
            account_id=data["account_id"]
        )
        if not standard_user_role:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Standard user role does not exist.")
                    )
                }
            )

        self.standard_user_role = standard_user_role
        self.account_member = account_member
        return data

    def _factory_account_access(self):
        data = self.data
        standard_user_role = self.standard_user_role
        add_account_access_to_profile(
            profile_id=data["profile_id"],
            role_id=standard_user_role.id,
            account_id=data["account_id"],
        )
        admin_account_access = create_admin_account_access(
            account_id=data["account_id"], member_id=self.account_member.id
        )
        return admin_account_access


class RemoveAdminMemberAccountAccess(ServiceBase):
    def __init__(self, data):
        self.data = data

    def execute(self):
        admin_account_access = self._validate_data()
        return self._remove_account_access(
            admin_account_access=admin_account_access
        )

    def _validate_data(self):
        data = run_validator(RemoveAccountAccessSerializer, self.data)
        admin_account_access = get_admin_account_access_by_id(
            account_access_id=data["account_access_id"]
        )

        if not admin_account_access:
            raise ValidationError(
                {"detail": ErrorDetail(_("Account access id is invalid."))}
            )
        return admin_account_access

    def _remove_account_access(self, admin_account_access):
        admin_account_access.expire_access()
