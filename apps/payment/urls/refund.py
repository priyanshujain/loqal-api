from apps.payment.views.refund import RefundListAPI

from django.urls import path


urlpatterns = [
    path(
        "merchant/refunds/",
        RefundListAPI.as_view(),
        name="merchant_refund_history",
    ),
]
