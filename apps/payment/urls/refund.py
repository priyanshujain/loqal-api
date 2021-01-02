from django.urls import path

from apps.payment.views.refund import RefundDetailsAPI, RefundListAPI

urlpatterns = [
    path(
        "merchant/refunds/<str:refund_id>",
        RefundDetailsAPI.as_view(),
        name="merchant_refund_details",
    ),
    path(
        "merchant/refunds/",
        RefundListAPI.as_view(),
        name="merchant_refund_history",
    ),
]
