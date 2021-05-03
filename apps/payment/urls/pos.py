from django.urls import path

from apps.payment.views.pos import PosPaymentDetailsAPI, PosPaymentHistoryAPI

urlpatterns = [
    path(
        "pos/details/<str:payment_id>/",
        PosPaymentDetailsAPI.as_view(),
        name="merchant_pos_payment_details",
    ),
    path(
        "pos/recent/",
        PosPaymentHistoryAPI.as_view(),
        name="merchant_pos_payments",
    ),
]
