from api import serializers
from apps.merchant.models import AccountMember, FeatureAccessRole, MemberInvite

__all__ = (
    "MemberInviteResponse",
    "AccountMemberResponse",
    "MemberInviteDetailsResponse",
    "FeatureAccessRoleResponse",
)


class FeatureAccessRoleResponse(serializers.ModelSerializer):
    class Meta:
        model = FeatureAccessRole
        fields = (
            "is_full_access",
            "payment_requests",
            "payment_history",
            "settlements",
            "disputes",
            "refunds",
            "customers",
            "qr_codes",
            "store_profile",
            "team_management",
        )


class MemberInviteResponse(serializers.ModelSerializer):
    invite_id = serializers.IntegerField(source="id", read_only=True)
    role = FeatureAccessRoleResponse(read_only=True)
    merchant_id = serializers.IntegerField(
        source="merchant.id", read_only=True
    )

    class Meta:
        model = MemberInvite
        fields = (
            "merchant_id",
            "first_name",
            "last_name",
            "email",
            "position",
            "invite_id",
            "role",
        )


class MemberInviteDetailsResponse(serializers.ModelSerializer):
    invite_id = serializers.IntegerField(source="id", read_only=True)
    role = FeatureAccessRoleResponse(read_only=True)
    company_name = serializers.CharField(
        source="account.company_name", read_only=True
    )

    class Meta:
        model = MemberInvite
        fields = (
            "first_name",
            "last_name",
            "email",
            "position",
            "invite_id",
            "role",
            "company_name",
        )


class AccountMemberResponse(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source="id", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    is_disbled = serializers.BooleanField(
        source="user.is_disabled", read_only=True
    )
    role = FeatureAccessRoleResponse(read_only=True)

    class Meta:
        model = AccountMember
        fields = (
            "member_id",
            "first_name",
            "last_name",
            "email",
            "position",
            "is_disbled",
            "role",
        )

