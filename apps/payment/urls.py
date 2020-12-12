from django.urls import path

from apps.payment.views import CreatePaymentAPI, PaymentHistoryAPI

urlpatterns = [
    path("create/", CreatePaymentAPI.as_view(), name="create_payment"),
    path("history/", PaymentHistoryAPI.as_view(), name="payment_history"),
]
