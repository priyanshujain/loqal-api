from api import serializers
from apps.notification.models import UserDevice
from apps.notification.options import UserDeviceTypes

__all__ = (
    "RegisterUserDeviceValidator",
    "UpdateUserDeviceTokenValidator",
)


class RegisterUserDeviceValidator(serializers.ModelSerializer):
    device_platform = serializers.ChoiceField(choices=UserDeviceTypes.choices)
    device_id = serializers.CharField()

    class Meta:
        model = UserDevice
        fields = (
            "device_name",
            "device_id",
            "build_number",
            "brand_name",
            "api_level",
            "fcm_token",
            "device_platform",
            "manufacturer",
        )
