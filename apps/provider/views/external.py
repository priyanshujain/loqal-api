from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from api.views import APIView
from apps.provider.services import ProcesssProviderWebhook


class ProviderWebhookAPI(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProviderWebhookAPI, self).dispatch(
            request, *args, **kwargs
        )

    def post(self, request, webhook_id):
        ProcesssProviderWebhook(
            headers=request.headers,
            request_data=self.request_data,
            request_body=self.request_body,
            webhook_id=webhook_id,
        ).handle()
        return self.response()
