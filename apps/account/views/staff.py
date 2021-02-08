from api.views import StaffAPIView
from apps.account.dbapi.staff import (get_active_non_loqal_merchants,
                                      get_loqal_consumers, get_loqal_merchants)
from apps.account.responses.staff import (ConsumerAccountProfileResponse,
                                          MerchantAccountProfileResponse)
from apps.account.services import (CreateNonLoqalMerchant, DisableAccount,
                                   EnableAccount)


class GetActiveMerchantsAPI(StaffAPIView):
    def get(self, request):
        merchants = get_loqal_merchants()
        return self.response(
            MerchantAccountProfileResponse(merchants, many=True).data
        )


class GetConsumersAPI(StaffAPIView):
    def get(self, request):
        consumers = get_loqal_consumers()
        return self.response(
            ConsumerAccountProfileResponse(consumers, many=True).data
        )


class CreateNonLoqalMerchantsAPI(StaffAPIView):
    def post(self, request):
        merchant_account = CreateNonLoqalMerchant(
            data=self.request_data
        ).handle()
        return self.response(
            MerchantAccountProfileResponse(merchant_account).data
        )


class DisableAccountAPI(StaffAPIView):
    def post(self, request):
        DisableAccount(data=self.request_data).handle()
        return self.response(status=204)


class EnableAccountAPI(StaffAPIView):
    def post(self, request):
        EnableAccount(data=self.request_data).handle()
        return self.response(status=204)


class GetNonLoqalMerchantsAPI(StaffAPIView):
    def get(self, request):
        merchants = get_active_non_loqal_merchants()
        return self.response(
            MerchantAccountProfileResponse(merchants, many=True).data
        )
