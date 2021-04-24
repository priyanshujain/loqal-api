from api import serializers
from apps.merchant.models import PosStaff

__all__ = (
    "CreatePosStaffResponse",
    "ListPosStaffResponse",
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
            "first_name",
            "last_name",
            "pos_staff_id",
            "email",
            "phone_number",
            "is_disabled",
            "login_pin",
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

    class Meta:
        model = PosStaff
        fields = (
            "first_name",
            "last_name",
            "pos_staff_id",
            "email",
            "phone_number",
            "is_disabled",
        )
