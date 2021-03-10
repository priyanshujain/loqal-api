from api.views import MerchantAPIView

__all__ = ("InviteConsumerAPI",)


class InviteConsumerAPI(MerchantAPIView):
    def post(self, request):
        account = request.merchant_account
        return self.response()
