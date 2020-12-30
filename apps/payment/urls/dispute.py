from django.urls import path

from apps.payment.views.dispute import DisputeListAPI

urlpatterns = [
    path(
        "merchant/disputes/",
        DisputeListAPI.as_view(),
        name="merchant_disputes_history",
    ),
]
