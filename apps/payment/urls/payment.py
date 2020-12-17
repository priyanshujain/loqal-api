from django.urls import path

from apps.payment.views.payment import (
    CreatePaymentAPI,
    PaymentHistoryAPI,
    CreatePaymentRequestAPI,
    ListMerchantPaymentRequestAPI,
    ListConsumerPaymentRequestAPI,
    ApprovePaymentRequestAPI,
    RejectPaymentRequestAPI,
)

urlpatterns = [
    path("create/", CreatePaymentAPI.as_view(), name="create_payment"),
    path("history/", PaymentHistoryAPI.as_view(), name="payment_history"),
    path(
        "request/create/",
        CreatePaymentRequestAPI.as_view(),
        name="create_payment_request",
    ),
    path(
        "request/approve/",
        ApprovePaymentRequestAPI.as_view(),
        name="approve_payment_request",
    ),
    path(
        "request/reject/",
        RejectPaymentRequestAPI.as_view(),
        name="reject_payment_request",
    ),
    path(
        "request/consumer/",
        ListConsumerPaymentRequestAPI.as_view(),
        name="consumer_payment_request",
    ),
    path(
        "request/merchant/",
        ListMerchantPaymentRequestAPI.as_view(),
        name="merchant_payment_request",
    ),
]
