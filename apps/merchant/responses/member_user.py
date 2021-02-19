from api import serializers
from apps.merchant.models import AccountMember

__all__ = ("MemberProfileResponse",)


class MemberProfileResponse(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    email_verified = serializers.BooleanField(
        source="user.email_verified", read_only=True
    )
    phone_number = serializers.CharField(
        source="user.phone_number", read_only=True
    )
    two_factor_auth = serializers.BooleanField(
        source="user.two_factor_auth", read_only=True
    )
    role_id = serializers.CharField(source="role.id", read_only=True)

    class Meta:
        model = AccountMember
        fields = (
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "two_factor_auth",
            "position",
            "account_active",
            "role_id",
            "is_primary_member",
            "phone_number",
        )
