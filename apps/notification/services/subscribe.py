from django.utils.translation import gettext as _

from api.helpers import run_validator
from api.services import ServiceBase
from apps.notification.dbapi import get_device_by_id, register_user_device
from apps.notification.validators import RegisterUserDeviceValidator

__all__ = ("SubscribePushNotication",)


class SubscribePushNotication(ServiceBase):
    def __init__(self, request, data):
        self.user = request.user
        self.request = request
        self.data = data

    def handle(self):
        data = self._validate_data()
        device_id = data["device_id"]
        user_device = get_device_by_id(
            user_id=self.user.id, device_id=device_id
        )
        if user_device:
            user_device.update_fcm_token(fcm_token=data["fcm_token"])
        else:
            user_device = self._factory_user_device(data)
        self.request.session["device_id"] = user_device.device_id
        self.request.session.modified = True
        return user_device

    def _validate_data(self):
        data = run_validator(RegisterUserDeviceValidator, self.data)
        return data

    def _factory_user_device(self, data):
        device_name = data.get("device_name", "")
        device_id = data.get("device_id")
        build_number = data.get("build_number", "")
        brand_name = data.get("brand_name", "")
        api_level = data.get("api_level")
        fcm_token = data.get("fcm_token")
        device_platform = data.get("device_platform")
        manufacturer = data.get("manufacturer", "")
        return register_user_device(
            user_id=self.user.id,
            device_id=device_id,
            device_name=device_name,
            build_number=build_number,
            brand_name=brand_name,
            api_level=api_level,
            fcm_token=fcm_token,
            device_platform=device_platform,
            manufacturer=manufacturer,
        )
