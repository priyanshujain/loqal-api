from api.views import MerchantAPIView
from apps.marketing.services import GetCampaigns


class GetMerchantCampaignsAPI(MerchantAPIView):
    def get(self, request):
        return self.response(GetCampaigns().handle())
