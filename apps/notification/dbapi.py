from django.db.utils import IntegrityError

from apps.notification.models import UserDevice
from apps.notification.options import UserDeviceTypes


def create_user_device(
    user_id,
    registration_id,
    device_type=None,
):
    if not device_type:
        device_type = UserDeviceTypes.ANDROID
    try:
        return UserDevice.objects.create(
            user_id=user_id,
            registration_id=registration_id,
            device_type=device_type,
        )
    except IntegrityError:
        return None
