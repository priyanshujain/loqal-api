from api import serializers
from apps.merchant.models import AccountMember, FeatureAccessRole

__all__ = ("MemberProfileResponse",)


class FeatureAccessRoleResponse(serializers.ModelSerializer):
    payment_requests = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    payment_history = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    settlements = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    disputes = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    refunds = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    customers = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    qr_codes = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    store_profile = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    team_management = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    bank_accounts = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    loyalty_program = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    top_customers = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )
    merchant_settings = serializers.ListField(
        child=serializers.EnumCharChoiceValueField(read_only=True)
    )

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
            "bank_accounts",
            "loyalty_program",
            "top_customers",
            "merchant_settings",
        )


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
    role = FeatureAccessRoleResponse(read_only=True)

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
            "role",
            "is_primary_member",
            "phone_number",
        )
