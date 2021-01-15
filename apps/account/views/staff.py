from api.views import StaffAPIView
from apps.account.dbapi.staff import (get_active_merchants,
                                      get_active_non_loqal_merchants)
from apps.account.responses.staff import MerchantAccountProfileResponse
from apps.account.services import CreateNonLoqalMerchant

__all__ = ("GetActiveMerchantsAPI",)


class GetActiveMerchantsAPI(StaffAPIView):
    def get(self, request):
        merchants = get_active_merchants()
        return self.response(
            MerchantAccountProfileResponse(merchants, many=True).data
        )


class CreateNonLoqalMerchantsAPI(StaffAPIView):
    def post(self, request):
        merchant_account = CreateNonLoqalMerchant(
            data=self.request_data
        ).handle()
        return self.response(
            MerchantAccountProfileResponse(merchant_account).data
        )


class GetNonLoqalMerchantsAPI(StaffAPIView):
    def get(self, request):
        merchants = get_active_non_loqal_merchants()
        return self.response(
            MerchantAccountProfileResponse(merchants, many=True).data
        )
