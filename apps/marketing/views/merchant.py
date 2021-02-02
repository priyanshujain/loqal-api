from api.views import MerchantAPIView
from apps.marketing.dbapi import get_active_campaigns
from apps.marketing.responses import CampaignResponse


class GetMerchantCampaignsAPI(MerchantAPIView):
    def post(self, request):
        campaigns = get_active_campaigns()
        self.response(CampaignResponse(campaigns, many=True).data)
