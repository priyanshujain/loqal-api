from api import serializers
from apps.merchant.models import (AccountMember, FeatureAccessRole,
                                  MemberInvite, PosStaff)

__all__ = (
    "MemberInviteResponse",
    "AccountMemberResponse",
    "MemberInviteDetailsResponse",
    "FeatureAccessRoleResponse",
    "PosStaffResponse",
)


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
    is_disabled = serializers.BooleanField(
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
            "is_disabled",
            "role",
        )


class PosStaffResponse(serializers.ModelSerializer):
    pos_staff_id = serializers.CharField(source="u_id", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    phone_number = serializers.CharField(
        source="user.phone_number", read_only=True
    )
    is_disabled = serializers.BooleanField(
        source="user.is_disabled", read_only=True
    )
    register_name = serializers.CharField(
        source="register.register_name", read_only=True
    )
    qrcode_id = serializers.CharField(
        source="register.qrcode_id", read_only=True
    )

    class Meta:
        model = PosStaff
        fields = (
            "pos_staff_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "is_disabled",
            "qrcode_id",
            "register_name",
        )
