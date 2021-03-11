from enum import unique

from django.conf import settings
from django.contrib.auth import default_app_config
from django.db import models
from django.utils import tree
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from apps.account.models import MerchantAccount
from apps.merchant.models import AccountMember
from db.models import AbstractBaseModel, BaseModel
from db.models.fields import ChoiceCharEnumField
from plugins.fcm import FcmPlugin

from .options import PaymentNotificationTypes, UserDeviceTypes


class UserDevice(BaseModel):
    """
    This represents user device for push notification
    """

    device_name = models.CharField(max_length=128, blank=True)
    device_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=None,
    )
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
        blank=True, null=True, default=None, max_length=32, unique=True
    )
    fcm_token = models.TextField()
    device_platform = ChoiceCharEnumField(
        enum_type=UserDeviceTypes, max_length=8
    )
    manufacturer = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "user_device"
        unique_together = (
            "user",
            "device_id",
        )

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

    def update_fcm_token(self, fcm_token, save=True):
        self.fcm_token = fcm_token
        self.active = True
        if save:
            self.save()

    def inactivate_device(self, save=True):
        self.active = False
        if save:
            self.save()

    def send_notification_message(
        self,
        title=None,
        body=None,
        icon=None,
        data_message=None,
        sound=None,
        badge=None,
        api_key=None,
        **kwargs
    ):
        """
        Send single notification message.
        """

        result = FcmPlugin(token=self.fcm_token).send_notification(
            title=title,
            body=body,
            icon=icon,
            data_message=data_message,
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

        result = FcmPlugin(token=self.fcm_token).send_data(
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


class StaffPaymentNotificationSetting(AbstractBaseModel):
    """
    This represents payment notification to staff
    """

    merchant = models.ForeignKey(
        MerchantAccount,
        on_delete=models.CASCADE,
    )
    staff = models.OneToOneField(
        AccountMember,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    phone_number = models.CharField(max_length=10, blank=True)
    phone_number_country = models.CharField(
        max_length=2, blank=True, default="US"
    )
    email = models.EmailField(blank=True)
    notification_type = ChoiceCharEnumField(
        enum_type=PaymentNotificationTypes,
        max_length=128,
        default=PaymentNotificationTypes.ALL,
    )
    sms_enabled = models.BooleanField(default=False)
    email_enabled = models.BooleanField(default=False)
    app_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "staff_payment_notification_setting"

    def disable(self, save=True):
        self.is_active = False
        if save:
            self.save()
