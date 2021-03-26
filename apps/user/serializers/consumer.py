from api import serializers
from apps.user.models import User


class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ("avatar",)

    def validate(self, data):
        if data.get("avatar") is None:
            raise serializers.ValidationError(
                {"detail": "No avatar image were provided"}
            )
        return data
