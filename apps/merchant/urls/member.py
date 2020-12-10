from django.urls import path

from apps.merchant.views.member import (CreateFeatureAccessRoleAPI,
                                        CreateMemberInviteAPI,
                                        DeleteFeatureAccessRoleAPI,
                                        DisableMemberAPI, EnableMemberAPI,
                                        FeatureAccessRolesDetailsAPI,
                                        GetMemberInvitesAPI,
                                        ListFeatureAccessRolesAPI,
                                        ListMembersAPI, MemberFeatureAcessAPI,
                                        MemberSignupAPI,
                                        ResendMemberInviteEmailAPI,
                                        UpdateFeatureAccessRoleAPI,
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
        "member/roles/<int:role_id>/",
        FeatureAccessRolesDetailsAPI.as_view(),
        name="member_role_details_api",
    ),
    path(
        "member/roles/create/",
        CreateFeatureAccessRoleAPI.as_view(),
        name="member_role_create_api",
    ),
    path(
        "member/roles/update/",
        UpdateFeatureAccessRoleAPI.as_view(),
        name="member_role_update_api",
    ),
    path(
        "member/oles/delete/",
        DeleteFeatureAccessRoleAPI.as_view(),
        name="member_role_delete_api",
    ),
    path(
        "member/roles/",
        ListFeatureAccessRolesAPI.as_view(),
        name="member_roles_api",
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
