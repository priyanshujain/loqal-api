from api.views import StaffAPIView
from apps.marketing.dbapi import get_all_campaigns
from apps.marketing.responses import CampaignResponse
from apps.marketing.services import CreateCampaign, UpdateCampaign


class CreateCampaignAPI(StaffAPIView):
    def post(self, request):
        campaign = CreateCampaign(data=self.request_data).handle()
        return self.response(CampaignResponse(campaign).data, status=201)


class UpdateCampaignAPI(StaffAPIView):
    def put(self, request):
        UpdateCampaign(data=self.request_data).handle()
        return self.response(status=204)


class GetCampaignsAPI(StaffAPIView):
    def get(self, request):
        campaigns = get_all_campaigns()
        return self.response(CampaignResponse(campaigns, many=True).data)
