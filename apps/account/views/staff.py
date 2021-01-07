from api.views import StaffAPIView
from apps.account.dbapi.staff import get_active_merchants
from apps.account.responses.staff import MerchantAccountProfileResponse

__all__ = ("GetActiveMerchantsAPI",)


class GetActiveMerchantsAPI(StaffAPIView):
    def get(self, request):
        merchants = get_active_merchants()
        return self.response(
            MerchantAccountProfileResponse(merchants, many=True).data
        )
