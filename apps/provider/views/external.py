from api.views import APIView
from apps.provider.services import ProcesssProviderWebhook


class ProviderWebhookAPI(APIView):
    def post(self, request, webhook_id):
        ProcesssProviderWebhook(
            headers=request.headers,
            request_data=self.request_data,
            request_body=self.request_body,
            webhook_id=webhook_id,
        ).handle()
        return self.response()
