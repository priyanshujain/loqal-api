from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import StaffAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.merchant.dbapi import get_account_invites, get_members_by_account
from apps.merchant.responses import AccountMemberResponse, MemberInviteResponse
from apps.merchant.services import (CreateMemberInvite, DisableMember,
                                    EnableMember,
                                    MemberSignupInviteEmailResend,
                                    UpdateFeatureAccessRole,
                                    UpdateMemberInvite, UpdateMemberRole)


class StaffMerchantBaseAPI(StaffAPIView):
    def validate_merchant(self, merchant_id):
        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_id
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return merchant_account


class CreateMemberInviteAPI(StaffMerchantBaseAPI):
    """
    Create new member invite api
    """

    def post(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        invite = self._run_services(merchant_id=merchant_id)
        return self.response(status=201, data={"id": invite.id})

    def _run_services(self, merchant_id):
        service = CreateMemberInvite(
            merchant_id=merchant_id, data=self.request_data
        )
        return service.handle()


class GetMemberInvitesAPI(StaffMerchantBaseAPI):
    """
    List member invites api
    """

    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        invites = get_account_invites(merchant_id)
        return self.response(MemberInviteResponse(invites, many=True).data)


class ResendMemberInviteEmailAPI(StaffMerchantBaseAPI):
    """
    Resend member invite email api
    """

    def post(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response(status=204)

    def _run_services(self, merchant_id):
        MemberSignupInviteEmailResend(
            merchant_id=merchant_id, data=self.request_data
        ).handle()


class UpdateMemberInviteAPI(StaffMerchantBaseAPI):
    """
    Update member invite api
    """

    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        _ = self._run_services(merchant_id=merchant_id)
        return self.response(status=204)

    def _run_services(self, merchant_id):
        return UpdateMemberInvite(
            merchant_id=merchant_id, data=self.request_data
        ).handle()


class UpdateMemberRoleAPI(StaffMerchantBaseAPI):
    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response(status=204)

    def _run_services(self, merchant_id):
        UpdateMemberRole(
            merchant_id=merchant_id, data=self.request_data
        ).handle()


class ListMembersAPI(StaffMerchantBaseAPI):
    def get(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        members = get_members_by_account(merchant_id=merchant_id)
        return self.response(AccountMemberResponse(members, many=True).data)


class DisableMemberAPI(StaffMerchantBaseAPI):
    def post(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response()

    def _run_services(self, merchant_id):
        DisableMember(merchant_id=merchant_id, data=self.request_data).handle()


class EnableMemberAPI(StaffMerchantBaseAPI):
    def post(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response()

    def _run_services(self, merchant_id):
        EnableMember(merchant_id=merchant_id, data=self.request_data).handle()


class UpdateFeatureAccessRoleAPI(StaffMerchantBaseAPI):
    def put(self, request, merchant_id):
        merchant_account = self.validate_merchant(merchant_id=merchant_id)
        merchant_id = merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response()

    def _run_services(self, merchant_id):
        UpdateFeatureAccessRole(
            merchant_id=merchant_id, data=self.request_data
        ).handle()
