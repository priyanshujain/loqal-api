from api import serializers
from apps.user.models import User

__all__ = ("AdminUserProfileResponse",)


class AdminUserProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "username",
            "two_factor_auth",
            "phone_number",
            "phone_number_verified",
            "user_type",
        )
