from api import serializers
from apps.merchant.models import PosStaff

__all__ = (
    "CreatePosStaffResponse",
    "ListPosStaffResponse",
    "ValidatePosStaffAccessTokenResponse",
)


class CreatePosStaffResponse(serializers.ModelSerializer):
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

    class Meta:
        model = PosStaff
        fields = (
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "pos_staff_id",
            "email",
            "phone_number",
            "is_disabled",
            "login_pin",
            "shift_start",
            "shift_end",
        )


class ListPosStaffResponse(serializers.ModelSerializer):
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
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "pos_staff_id",
            "email",
            "phone_number",
            "is_disabled",
            "qrcode_id",
            "register_name",
            "shift_start",
            "shift_end",
        )


class ValidatePosStaffAccessTokenResponse(serializers.ModelSerializer):
    is_disabled = serializers.BooleanField(
        source="user.is_disabled", read_only=True
    )
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = PosStaff
        fields = (
            "login_token_expire_time",
            "username",
            "is_disabled",
        )
