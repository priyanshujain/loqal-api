from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import ConsumerAPIView
from apps.account.dbapi import get_merchant_account_by_uid
from apps.account.responses import MerchantDetailsResponse

__all__ = ("MerchantBasicDetailsAPI",)


class MerchantBasicDetailsAPI(ConsumerAPIView):
    def get(self, request):
        merchant_uid = self.request_data.get("merchant_id", None)
        if not merchant_uid:
            raise ValidationError(
                {"detail": ErrorDetail(_("merchant_id is required."))}
            )

        merchant_account = get_merchant_account_by_uid(
            merchant_uid=merchant_uid
        )
        if not merchant_account:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant."))}
            )
        return self.response(MerchantDetailsResponse(merchant_account).data)


class RecentMerchantsAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        return self.response()
