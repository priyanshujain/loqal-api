from api import serializers
from apps.user.models import User

__all__ = ("UserProfileResponse",)


class UserProfileResponse(serializers.ModelSerializer):
    email_verified = serializers.BooleanField(
        source="user.email_verified", read_only=True
    )
    two_factor_auth = serializers.BooleanField(
        source="user.two_factor_auth", read_only=True
    )
    email = serializers.CharField(source="user.email", read_only=True)
    position = serializers.CharField(
        source="accountmember.position", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "two_factor_auth",
            "contact_number",
            "position",
        )
