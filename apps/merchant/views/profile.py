from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import MerchantAPIView
from apps.merchant.responses import MerchantProfileResponse
from apps.merchant.services import UpdateMerchantProfile

__all__ = (
    "UpdateMerchantProfileAPI",
    "GetMerchantProfileAPI",
)


class UpdateMerchantProfileAPI(MerchantAPIView):
    def put(self, request):
        merchant_account = request.merchant_account
        UpdateMerchantProfile(
            merchant_id=merchant_account.id, data=self.request_data
        ).handle()
        return self.response(status=204)


class GetMerchantProfileAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        try:
            merchant_profile = merchant_account.merchantprofile
        except AttributeError:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid merchant profile."))}
            )
        return self.response(MerchantProfileResponse(merchant_profile).data)
