from api import serializers
from apps.notification.models import UserDevice


class RegisterUserDeviceResponse(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = (
            "device_name",
            "device_id",
            "device_tracking_id",
        )
