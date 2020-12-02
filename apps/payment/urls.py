from django.urls import path

from apps.payment.views import (CreatePaymentAPI, ListPaymentAproversAPI,
                                ListPendingPaymentRequestAPI,
                                ListRejectedPaymentRequestAPI,
                                ListTransactionsAPI, PaymentRequestDetailAPI,
                                TransactionConfirmationFileAPI,
                                TransactionDetailsAPI)

urlpatterns = [
    path("create/", CreatePaymentAPI.as_view(), name="create_payment"),
    path("transactions/", ListTransactionsAPI.as_view(),),
    path(
        "transactions/<int:transaction_id>/", TransactionDetailsAPI.as_view(),
    ),
    path("pending/", ListPendingPaymentRequestAPI.as_view(),),
    path("rejected/", ListRejectedPaymentRequestAPI.as_view(),),
    path("approvers/", ListPaymentAproversAPI.as_view(),),
    path(
        "transactions/<int:transaction_id>/transaction-confirmation/",
        TransactionConfirmationFileAPI.as_view(),
    ),
    path(
        "pending/<int:payment_request_id>/", PaymentRequestDetailAPI.as_view(),
    ),
]
