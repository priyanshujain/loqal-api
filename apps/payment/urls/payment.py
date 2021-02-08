from django.urls import path

from apps.payment.views.merchant_payment import MerchantPaymentHistoryAPI
from apps.payment.views.payment import (ApprovePaymentRequestAPI,
                                        CreatePaymentAPI,
                                        CreatePaymentRequestAPI,
                                        CreateRefundPaymentAPI,
                                        ListConsumerPaymentRequestAPI,
                                        ListMerchantPaymentRequestAPI,
                                        PaymentHistoryAPI, RecentStoresAPI,
                                        RejectPaymentRequestAPI,
                                        TransactionDetailsAPI)
from apps.payment.views.settlements import (ListMerchantSettlementsAPI,
                                            MerchantSettlementDetailsAPI)

urlpatterns = [
    path("create/", CreatePaymentAPI.as_view(), name="create_payment"),
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
    path(
        "history/merchant/",
        MerchantPaymentHistoryAPI.as_view(),
        name="merchant_payment_history",
    ),
    path("history/", PaymentHistoryAPI.as_view(), name="payment_history"),
    path(
        "refund/",
        CreateRefundPaymentAPI.as_view(),
        name="create_refund_payment",
    ),
    path(
        "transactions/details/<str:transaction_id>/",
        TransactionDetailsAPI.as_view(),
        name="consumer_transaction_details",
    ),
    path(
        "recent-stores/",
        RecentStoresAPI.as_view(),
        name="recent_stores",
    ),
    path(
        "settlements/<str:settlement_id>/",
        MerchantSettlementDetailsAPI.as_view(),
        name="merchant_settlement_details",
    ),
    path(
        "settlements/",
        ListMerchantSettlementsAPI.as_view(),
        name="merchant_settlements",
    ),
]
