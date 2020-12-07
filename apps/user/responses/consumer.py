from django.contrib.auth import models
from api import serializers
from apps.user.models import User
from apps.box.models import BoxFile

__all__ = ("UserProfileResponse",)


class AvatarFileResponse(serializers.ModelSerializer):
    class Meta:
        model = BoxFile
        fields = (
            "id",
            "file_name",            
        )

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
    avatar_file = AvatarFileResponse()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "two_factor_auth",
            "phone_number",
            "position",
            "avatar_file",
        )
