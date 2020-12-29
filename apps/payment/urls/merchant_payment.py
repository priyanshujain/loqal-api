from django.urls import path

from apps.payment.views.merchant_payment import MerchantPaymentDetailsAPI

urlpatterns = [
    path(
        "details/<str:payment_id>/",
        MerchantPaymentDetailsAPI.as_view(),
        name="merchant_payment_details",
    ),
]
