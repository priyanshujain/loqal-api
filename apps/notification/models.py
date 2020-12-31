from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from db.models import BaseModel
from db.models.fields import ChoiceCharEnumField

from .options import UserDeviceTypes
from .tasks import (
    fcm_send_single_device_data_message,
    fcm_send_single_device_notification_message,
)
from django.utils.crypto import get_random_string


class UserDevice(BaseModel):
    """
    This represents user device for push notification
    """

    device_name = models.CharField(max_length=128, blank=True)
    device_id = models.CharField(max_length=128, blank=True)
    build_number = models.CharField(max_length=32, blank=True)
    brand_name = models.CharField(max_length=128, blank=True)
    api_level = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    device_tracking_id = models.CharField(
        blank=True, null=True, default=None, unique=True, max_length=32
    )
    fcm_token = models.TextField()
    device_platform = ChoiceCharEnumField(enum_type=UserDeviceTypes, max_length=8)
    manufacturer = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "user_device"

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.device_tracking_id:
            self.device_tracking_id = id_generator()
            while UserDevice.objects.filter(
                device_tracking_id=self.device_tracking_id
            ).exists():
                self.device_tracking_id = id_generator()
        return super().save(*args, **kwargs)

    def send_notification_message(
        self,
        title=None,
        body=None,
        icon=None,
        data=None,
        sound=None,
        badge=None,
        api_key=None,
        **kwargs
    ):
        """
        Send single notification message.
        """

        result = fcm_send_single_device_notification_message(
            registration_id=str(self.fcm_token),
            title=title,
            body=body,
            icon=icon,
            data=data,
            sound=sound,
            badge=badge,
            api_key=api_key,
            **kwargs
        )
        return result

    def send_data_message(
        self,
        condition=None,
        collapse_key=None,
        delay_while_idle=False,
        time_to_live=None,
        restricted_package_name=None,
        low_priority=False,
        dry_run=False,
        data_message=None,
        content_available=None,
        api_key=None,
        timeout=5,
        json_encoder=None,
    ):
        """
        Send single data message.
        """

        result = fcm_send_single_device_data_message(
            registration_id=str(self.fcm_token),
            condition=condition,
            collapse_key=collapse_key,
            delay_while_idle=delay_while_idle,
            time_to_live=time_to_live,
            restricted_package_name=restricted_package_name,
            low_priority=low_priority,
            dry_run=dry_run,
            data_message=data_message,
            content_available=content_available,
            api_key=api_key,
            timeout=timeout,
            json_encoder=json_encoder,
        )
        return result
