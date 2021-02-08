from api import serializers
from apps.user.options import UserType

__all__ = (
    "AdminUserAddSerializer",
    "AdminRoleChangeSerializer",
)


class AdminUserAddSerializer(serializers.ValidationSerializer):
    user_email = serializers.EmailField()
    password = serializers.CharField(max_length=64)
    user_type = serializers.ChoiceField(choices=UserType.choices())
    first_name = serializers.CharField(max_length=254)
    last_name = serializers.CharField(max_length=254)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user_email"] = str(attrs["user_email"]).lower()
        return attrs


class AdminRoleChangeSerializer(serializers.ValidationSerializer):
    user_email = serializers.EmailField()
    user_type = serializers.ChoiceField(choices=UserType.choices())

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user_email"] = str(attrs["user_email"]).lower()
        return attrs
