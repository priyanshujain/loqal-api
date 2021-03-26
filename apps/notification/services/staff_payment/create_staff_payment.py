from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.merchant.dbapi import get_account_member_by_id
from apps.notification.dbapi import (
    create_staff_payment_notification_setting,
    get_staff_payment_notification_setting_by_staff)
from apps.notification.validators import \
    CreateStaffPaymentNotificationSettingValidator

__all__ = ("CreateStaffPaymentNoticationSetting",)


class CreateStaffPaymentNoticationSetting(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self._validate_data()
        notification_setting = self._factory_payment_notification_setting(data)
        return notification_setting

    def _validate_data(self):
        data = run_validator(
            CreateStaffPaymentNotificationSettingValidator, self.data
        )
        staff_id = data["staff_id"]
        staff = get_account_member_by_id(
            member_id=staff_id, merchant_id=self.merchant.id
        )
        if not staff:
            raise ValidationError(
                {"detail": ErrorDetail(_("Staff member is not valid"))}
            )
        staff_setting = get_staff_payment_notification_setting_by_staff(
            merchant_id=self.merchant.id, staff_id=staff.id
        )
        if staff_setting:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Staff member is already registered for notification."
                        )
                    )
                }
            )
        data["phone_number"] = staff.user.phone_number
        return data

    def _factory_payment_notification_setting(self, data):
        notification_type = data.get("notification_type", "")
        staff_id = data.get("staff_id")
        sms_enabled = data.get("sms_enabled", "")
        email_enabled = data.get("email_enabled", "")
        return create_staff_payment_notification_setting(
            merchant_id=self.merchant.id,
            staff_id=staff_id,
            notification_type=notification_type,
            email_enabled=email_enabled,
            sms_enabled=sms_enabled,
        )
