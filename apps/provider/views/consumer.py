from api.views import LoggedInAPIView
from apps.provider.dbapi import get_all_payment_providers
from apps.provider.responses import PaymentProviderResponse


class ListPaymentProviderAPI(LoggedInAPIView):
    def get(self, request):
        payment_providers = get_all_payment_providers()
        return self.response(
            PaymentProviderResponse(payment_providers, many=True).data
        )
