from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.constants import DEFAULT_ROLES
from apps.merchant.dbapi import (check_if_roles_exists_by_name,
                                 check_invites_exists_by_role,
                                 check_members_exists_by_role,
                                 create_feature_access_role,
                                 get_feature_access_role_by_id,
                                 update_feature_access_role)
from apps.merchant.validators import (CreateFeatureAccessRoleValidator,
                                      DeleteFeatureAccessRoleValidator,
                                      UpdateFeatureAccessRoleValidator)

__all__ = (
    "CreateFeatureAccessRole",
    "CreateDefaultRoles",
    "UpdateFeatureAccessRole",
    "DeleteFeatureAccessRole",
)


class CreateDefaultRoles(ServiceBase):
    def __init__(self, merchant_id):
        self.merchant_id = merchant_id

    def handle(self):
        for member_role in DEFAULT_ROLES:
            role_name = member_role["role_name"]
            description = member_role["description"]
            team_and_roles = member_role["team_and_roles"]
            beneficiaries = member_role["beneficiaries"]
            transactions = member_role["transactions"]
            banking = member_role["banking"]
            settings = member_role["settings"]
            is_editable = member_role.get("is_editable", True)
            is_standard_user = member_role.get("is_standard_user", False)
            is_super_admin = member_role.get("is_super_admin", False)

            create_feature_access_role(
                merchant_id=self.merchant_id,
                role_name=role_name,
                description=description,
                team_and_roles=team_and_roles,
                beneficiaries=beneficiaries,
                transactions=transactions,
                banking=banking,
                settings=settings,
                is_editable=is_editable,
                is_standard_user=is_standard_user,
                is_super_admin=is_super_admin,
            )


class CreateFeatureAccessRole(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def _validate_data(self):
        data = run_validator(
            validator=CreateFeatureAccessRoleValidator, data=self.data
        )
        role_name = data["role_name"]
        if check_if_roles_exists_by_name(
            role_name=role_name, merchant_id=self.merchant_id
        ):
            raise ValidationError(
                {
                    "role_name": [
                        ErrorDetail(_("Role with this name already exists."))
                    ]
                }
            )
        self.data = data

    def handle(self):
        self._validate_data()
        data = self.data
        role_name = data["role_name"]
        description = data["description"]
        teams_and_roles = data["team_and_roles"]
        beneficiaries = data["beneficiaries"]
        transactions = data["transactions"]
        banking = data["banking"]
        settings = data["settings"]

        role = create_feature_access_role(
            merchant_id=self.merchant_id,
            role_name=role_name,
            description=description,
            team_and_roles=teams_and_roles,
            beneficiaries=beneficiaries,
            transactions=transactions,
            banking=banking,
            settings=settings,
        )
        return role


class UpdateFeatureAccessRole(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def validate_data(self):
        data = run_validator(
            validator=UpdateFeatureAccessRoleValidator, data=self.data
        )
        role_id = data["role_id"]
        role = get_feature_access_role_by_id(
            role_id=role_id, merchant_id=self.merchant_id
        )
        if not role:
            raise ValidationError(
                {"role_id": [ErrorDetail(_("Invalid role_id."))]}
            )

        self.data = data
        self.role = role

    def handle(self):
        self.validate_data()

        data = self.data
        description = data["description"]
        teams_and_roles = data["team_and_roles"]
        beneficiaries = data["beneficiaries"]
        transactions = data["transactions"]
        banking = data["banking"]
        settings = data["settings"]

        role = update_feature_access_role(
            role=self.role,
            description=description,
            team_and_roles=teams_and_roles,
            beneficiaries=beneficiaries,
            transactions=transactions,
            banking=banking,
            settings=settings,
        )
        return role


class DeleteFeatureAccessRole(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def _validate_data(self):
        data = run_validator(
            validator=DeleteFeatureAccessRoleValidator, data=self.data
        )

        role_id = data["role_id"]
        role = get_feature_access_role_by_id(
            role_id=role_id, merchant_id=self.merchant_id
        )
        if not role:
            raise ValidationError(
                {"role_id": [ErrorDetail(_("Invalid role_id."))]}
            )

        if check_members_exists_by_role(
            role_id=role_id, merchant_id=self.merchant_id
        ):
            raise ValidationError(
                {"detail": ErrorDetail(_("Members exist with this role."))}
            )

        if check_invites_exists_by_role(
            role_id=role_id, merchant_id=self.merchant_id
        ):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Member invites exist with this role.")
                    )
                }
            )

        self.role = role

    def handle(self):
        self._validate_data()
        self.role.delete()
