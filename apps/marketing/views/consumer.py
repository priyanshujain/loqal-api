from api.views import ConsumerAPIView
from apps.marketing.services import GetCampaigns


class GetConsumerCampaignsAPI(ConsumerAPIView):
    def get(self, request):
        return self.response(GetCampaigns().handle())
