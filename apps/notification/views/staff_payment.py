from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import MerchantAPIView
from apps.notification.dbapi import (
    get_all_staff_payment_notification_setting,
    get_staff_payment_notification_setting)
from apps.notification.responses import StaffPaymentNotificationSettingResponse
from apps.notification.services import CreateStaffPaymentNoticationSetting


class AddStaffNoticationSettingAPI(MerchantAPIView):
    def post(self, request):
        notification_setting = CreateStaffPaymentNoticationSetting(
            merchant=request.merchant_account,
            data=self.request_data,
        ).handle()
        return self.response(
            StaffPaymentNotificationSettingResponse(notification_setting).data
        )


class GetStaffNoticationSettingAPI(MerchantAPIView):
    def get(self, request):
        notification_settings = get_all_staff_payment_notification_setting(
            merchant_id=request.merchant_account.id
        )
        return self.response(
            StaffPaymentNotificationSettingResponse(
                notification_settings, many=True
            ).data
        )


class DisableStaffNoticationSettingAPI(MerchantAPIView):
    def post(self, request, setting_id):
        notification_setting = get_staff_payment_notification_setting(
            setting_id=setting_id, merchant_id=request.merchant_account.id
        )

        if not notification_setting:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid notification setting id."))}
            )

        notification_setting.disable()
        return self.response()


class DeleteStaffNoticationSettingAPI(MerchantAPIView):
    def post(self, request, setting_id):
        notification_setting = get_staff_payment_notification_setting(
            setting_id=setting_id, merchant_id=request.merchant_account.id
        )

        if not notification_setting:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid notification setting id."))}
            )

        notification_setting.delete()
        return self.response()
