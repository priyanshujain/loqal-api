from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import APIView, MerchantAPIView
from apps.merchant.dbapi import (
    get_account_invites,
    get_feature_access_role_by_id,
    get_feature_access_roles_by_account,
    get_member_invite_by_token,
    get_members_by_account,
)
from apps.merchant.responses import (
    MemberInviteResponse,
    AccountMemberResponse,
    FeatureAccessRoleResponse,
    MemberInviteDetailsResponse,
)
from apps.merchant.services import (
    CreateFeatureAccessRole,
    CreateMemberInvite,
    DeleteFeatureAccessRole,
    DisableMember,
    EnableMember,
    MemberSignup,
    MemberSignupInviteEmailResend,
    UpdateFeatureAccessRole,
    UpdateMemberInvite,
    UpdateMemberRole,
)


class CreateMemberInviteAPI(MerchantAPIView):
    """
    Create new member invite api
    """

    def post(self, request):
        merchant_id = request.merchant_account.id
        invite = self._run_services(merchant_id=merchant_id)
        return self.response(status=201, data={"id": invite.id})

    def _run_services(self, merchant_id):
        service = CreateMemberInvite(merchant_id=merchant_id, data=self.request_data)
        return service.handle()


class GetMemberInvitesAPI(MerchantAPIView):
    """
    List member invites api
    """

    def get(self, request):
        merchant_id = request.merchant_account.id
        invites = get_account_invites(merchant_id)
        return self.response(MemberInviteResponse(invites, many=True).data)


class VerifyMemberInviteAPI(APIView):
    """
    Verify signup invite by given key api
    """

    def get(self, request):
        token = request.GET.get("key", None)
        if not token:
            raise ValidationError({"key": [ErrorDetail(_("Key is required."))]})

        invite = get_member_invite_by_token(token=token)
        if not invite:
            raise ValidationError({"key": [ErrorDetail(_("Invalid key."))]})

        if invite.is_expired:
            raise ValidationError({"key": [ErrorDetail(_("Key expired."))]})

        return self.response(MemberInviteDetailsResponse(invite).data)


class ResendMemberInviteEmailAPI(MerchantAPIView):
    """
    Resend member invite email api
    """

    def post(self, request):
        merchant_id = request.merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response(status=204)

    def _run_services(self, merchant_id):
        MemberSignupInviteEmailResend(
            merchant_id=merchant_id, data=self.request_data
        ).handle()


class UpdateMemberInviteAPI(MerchantAPIView):
    """
    Update member invite api
    """

    def put(self, request):
        merchant_id = request.merchant_account.id
        _ = self._run_services(merchant_id=merchant_id)
        return self.response(status=204)

    def _run_services(self, merchant_id):
        return UpdateMemberInvite(
            merchant_id=merchant_id, data=self.request_data
        ).handle()


class MemberSignupAPI(APIView):
    """
    registration for new team member
    """

    def post(self, request):
        self._run_services()
        return self.response(status=201)

    def _run_services(self):
        MemberSignup(data=self.request_data).handle()


class UpdateMemberRoleAPI(MerchantAPIView):
    def put(self, request):
        merchant_id = request.merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response(status=204)

    def _run_services(self, merchant_id):
        UpdateMemberRole(merchant_id=merchant_id, data=self.request_data).handle()


class ListMembersAPI(MerchantAPIView):
    def get(self, request):
        merchant_id = request.merchant_account.id
        members = get_members_by_account(merchant_id=merchant_id)
        return self.response(AccountMemberResponse(members, many=True).data)


class DisableMemberAPI(MerchantAPIView):
    def post(self, request):
        merchant_id = request.merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response()

    def _run_services(self, merchant_id):
        DisableMember(merchant_id=merchant_id, data=self.request_data).handle()


class EnableMemberAPI(MerchantAPIView):
    def post(self, request):
        merchant_id = request.merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response()

    def _run_services(self, merchant_id):
        EnableMember(merchant_id=merchant_id, data=self.request_data).handle()


class ListFeatureAccessRolesAPI(MerchantAPIView):
    def get(self, request):
        merchant_id = request.merchant_account.id
        roles = get_feature_access_roles_by_account(merchant_id=merchant_id)
        return self.response(FeatureAccessRoleResponse(roles, many=True).data)


class FeatureAccessRolesDetailsAPI(MerchantAPIView):
    def get(self, request, role_id):
        merchant_id = request.merchant_account.id
        role = get_feature_access_role_by_id(role_id=role_id, merchant_id=merchant_id)
        if not role:
            raise ValidationError({"role_id": [ErrorDetail(_("Invalid role_id."))]})
        return self.response(FeatureAccessRoleResponse(role).data)


class CreateFeatureAccessRoleAPI(MerchantAPIView):
    def post(self, request):
        merchant_id = request.merchant_account.id
        role = self._run_services(merchant_id=merchant_id)
        return self.response(status=201, data={"role_id": role.id})

    def _run_services(self, merchant_id):
        return CreateFeatureAccessRole(
            merchant_id=merchant_id, data=self.request_data
        ).handle()


class UpdateFeatureAccessRoleAPI(MerchantAPIView):
    def put(self, request):
        merchant_id = request.merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response()

    def _run_services(self, merchant_id):
        UpdateFeatureAccessRole(
            merchant_id=merchant_id, data=self.request_data
        ).handle()


class MemberFeatureAcessAPI(MerchantAPIView):
    def get(self, request):
        member = request.merchant_account_member
        if not member.role:
            raise ValidationError({"detail": ErrorDetail("Role not found.")})

        return self.response(FeatureAccessRoleResponse(member.role).data)


class DeleteFeatureAccessRoleAPI(MerchantAPIView):
    def post(self, request):
        merchant_id = request.merchant_account.id
        self._run_services(merchant_id=merchant_id)
        return self.response()

    def _run_services(self, merchant_id):
        DeleteFeatureAccessRole(
            merchant_id=merchant_id, data=self.request_data
        ).handle()
