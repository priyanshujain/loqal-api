from api import serializers
from apps.merchant.models import AccountMember, FeatureAccessRole, MemberInvite

__all__ = (
    "MemberInviteResponse",
    "AccountMemberResponse",
    "MemberInviteDetailsResponse",
    "FeatureAccessRoleResponse",
)


class RoleInfoResponse(serializers.ModelSerializer):
    role_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = FeatureAccessRole
        fields = (
            "role_id",
            "role_name",
        )


class MemberInviteResponse(serializers.ModelSerializer):
    invite_id = serializers.IntegerField(source="id", read_only=True)
    role = RoleInfoResponse(read_only=True)

    class Meta:
        model = MemberInvite
        fields = "__all__"


class MemberInviteDetailsResponse(serializers.ModelSerializer):
    invite_id = serializers.IntegerField(source="id", read_only=True)
    role = RoleInfoResponse(read_only=True)
    company_name = serializers.CharField(
        source="account.company_name", read_only=True
    )

    class Meta:
        model = MemberInvite
        fields = "__all__"


class AccountMemberResponse(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source="id", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(
        source="user.last_name", read_only=True
    )
    email = serializers.CharField(source="profile.user.email", read_only=True)
    is_disbled = serializers.BooleanField(
        source="user.is_disabled", read_only=True
    )
    role = RoleInfoResponse(read_only=True)

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


class FeatureAccessRoleResponse(serializers.ModelSerializer):
    role_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = FeatureAccessRole
        fields = "__all__"
