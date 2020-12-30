from django.urls import path

from apps.payment.views.refund import RefundListAPI

urlpatterns = [
    path(
        "merchant/refunds/",
        RefundListAPI.as_view(),
        name="merchant_refund_history",
    ),
]
