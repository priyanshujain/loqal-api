from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.constants import DEFAULT_ROLE
from apps.merchant.dbapi import (create_member_invite, create_member_role,
                                 get_feature_access_role_by_id,
                                 get_member_invite_by_email,
                                 get_member_invite_by_id, update_member_invite,
                                 update_member_role)
from apps.merchant.notifications import MemberSignupInviteEmail
from apps.merchant.validators import (MemberInviteValidator,
                                      UpdateMemberInviteValidator)
from apps.user.dbapi import get_merchant_user_by_email

__all__ = (
    "CreateMemberInvite",
    "MemberSignupInviteEmailResend",
    "UpdateMemberInvite",
)


class CreateMemberInvite(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def _validate_data(self):
        data = run_validator(validator=MemberInviteValidator, data=self.data)
        email = data["email"]
        user = get_merchant_user_by_email(email=email)
        if user:
            raise ValidationError(
                {
                    "email": [
                        ErrorDetail(_("User already exists with this email."))
                    ]
                }
            )

        invite = get_member_invite_by_email(email=email)
        if invite:
            raise ValidationError(
                {"detail": ErrorDetail(_("User has already been invited."))}
            )

    def handle(self):
        self._validate_data()
        data = self.data
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        position = data["position"]
        role = data["role"]
        is_full_access = role["is_full_access"]
        member_role = None
        if is_full_access:
            data = DEFAULT_ROLE
            data["is_full_access"] = True
            member_role = create_member_role(data=data)
        else:
            member_role = create_member_role(data=role)

        invite = create_member_invite(
            merchant_id=self.merchant_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            position=position,
            role_id=member_role.id,
        )
        MemberSignupInviteEmail(invite=invite).send()
        return invite


class MemberSignupInviteEmailResend(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def _validate_data(self):
        data = self.data
        invite_id = data.get("invite_id")
        if not invite_id:
            raise ValidationError(
                {"invite_id": [ErrorDetail(_("This field is required."))]}
            )
        invite = get_member_invite_by_id(
            invite_id=invite_id, merchant_id=self.merchant_id
        )
        if not invite:
            raise ValidationError(
                {"invite_id": [ErrorDetail(_("Invalid invite_id."))]}
            )
        if invite.is_expired:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invite has been expired."))}
            )

        self.invite = invite

    def handle(self):
        self._validate_data()
        invite = self.invite
        MemberSignupInviteEmail(invite=invite).send()


class UpdateMemberInvite(ServiceBase):
    def __init__(self, merchant_id, data):
        self.merchant_id = merchant_id
        self.data = data

    def _validate_data(self):
        data = run_validator(
            validator=UpdateMemberInviteValidator, data=self.data
        )
        invite_id = data["invite_id"]

        invite = get_member_invite_by_id(
            invite_id=invite_id, merchant_id=self.merchant_id
        )
        if not invite:
            raise ValidationError(
                {"invite_id": [ErrorDetail(_("Invalid invite_id."))]}
            )
        if invite.is_expired:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invite already expired."))}
            )
        self.invite = invite

    def handle(self):
        self._validate_data()
        data = self.data
        invite = self.invite

        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        role = data["role"]
        position = data["position"]
        update_member_role(role_id=invite.role.id, data=role)
        invite = update_member_invite(
            invite=invite,
            first_name=first_name,
            last_name=last_name,
            email=email,
            position=position,
        )
        return invite
