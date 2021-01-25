from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.notification.dbapi import get_device_by_id
from apps.notification.validators import UnSubscribeUserDeviceValidator

__all__ = ("UnSubscribePushNotication",)


class UnSubscribePushNotication(ServiceBase):
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
            user_device.inactivate_device()
        else:
            raise ValidationError(
                {
                    "detail": [
                        ErrorDetail(
                            _("Device has already been un-subscribed.")
                        )
                    ]
                }
            )
        self.request.session["device_id"] = None
        self.request.session.modified = True
        return user_device

    def _validate_data(self):
        data = run_validator(UnSubscribeUserDeviceValidator, self.data)
        return data
