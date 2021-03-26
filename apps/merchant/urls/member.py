from django.urls import path

from apps.merchant.views.member import (CreateMemberInviteAPI,
                                        DisableMemberAPI, EnableMemberAPI,
                                        GetMemberInvitesAPI, ListMembersAPI,
                                        MemberFeatureAcessAPI, MemberSignupAPI,
                                        ResendMemberInviteEmailAPI,
                                        UpdateMemberInviteAPI,
                                        UpdateMemberRoleAPI,
                                        VerifyMemberInviteAPI)

urlpatterns = [
    path(
        "member/validate-invite/",
        VerifyMemberInviteAPI.as_view(),
        name="validate_invite_api",
    ),
    path(
        "member/update-invite/",
        UpdateMemberInviteAPI.as_view(),
        name="update_invite_api",
    ),
    path(
        "member/resend-invite/",
        ResendMemberInviteEmailAPI.as_view(),
        name="resend_invite_api",
    ),
    path(
        "member/disable/",
        DisableMemberAPI.as_view(),
        name="disable_member_api",
    ),
    path(
        "member/enable/",
        EnableMemberAPI.as_view(),
        name="enable_member_api",
    ),
    path(
        "member/invite/create/",
        CreateMemberInviteAPI.as_view(),
        name="create_member_invite_api",
    ),
    path(
        "member/invite/",
        GetMemberInvitesAPI.as_view(),
        name="get_member_invites_api",
    ),
    path(
        "member/signup/", MemberSignupAPI.as_view(), name="member_signup_api"
    ),
    path(
        "member/feature-access/update/",
        UpdateMemberRoleAPI.as_view(),
        name="member_feature_access_api",
    ),
    path(
        "member/feature-access/",
        MemberFeatureAcessAPI.as_view(),
        name="member_feature_access_api",
    ),
    path("member/", ListMembersAPI.as_view(), name="list_member_api"),
]
