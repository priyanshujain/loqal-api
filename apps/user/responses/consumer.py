from django.contrib.auth import models

from api import serializers
from apps.box.models import BoxFile
from apps.user.models import User

__all__ = ("UserProfileResponse",)


class AvatarFileResponse(serializers.ModelSerializer):
    class Meta:
        model = BoxFile
        fields = (
            "id",
            "file_name",
        )


class UserProfileResponse(serializers.ModelSerializer):
    avatar_file = AvatarFileResponse()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "two_factor_auth",
            "phone_number",
            "phone_number_verified",
            "avatar_file",
        )
