from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.notification.dbapi import get_device_by_id
from apps.notification.validators import UpdateUserDeviceTokenValidator

__all__ = ("UpdateDeviceToken",)


class UpdateDeviceToken(ServiceBase):
    def __init__(self, user, data):
        self.user = user
        self.data = data

    def handle(self):
        data = self._validate_data()
        user_device = data["user_device"]
        user_device.update_fcm_token(fcm_token=data["fcm_token"])

    def _validate_data(self):
        data = run_validator(UpdateUserDeviceTokenValidator, self.data)
        device_id = data["device_id"]
        user_device = get_device_by_id(
            user_id=self.user.id, device_id=device_id
        )
        if not user_device:
            raise ValidationError(
                {
                    "device_id": ErrorDetail(
                        "No device exists with this device_id."
                    )
                }
            )
        data["user_device"] = user_device
        return data
