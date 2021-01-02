from api import serializers
from apps.user.models import User

__all__ = ("UserProfileResponse",)


class UserProfileResponse(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "two_factor_auth",
        )
