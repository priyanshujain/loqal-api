from apps.payment.views.dispute import DisputeListAPI

from django.urls import path


urlpatterns = [
    path(
        "merchant/disputes/",
        DisputeListAPI.as_view(),
        name="merchant_disputes_history",
    ),
]
