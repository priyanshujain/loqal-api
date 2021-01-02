from django.urls import path

from apps.payment.views.dispute import (ConsumerDisputeDetailsAPI,
                                        CreateDisputeAPI, DisputeListAPI,
                                        DisputeReasonTypesAPI,
                                        MerchantDisputeDetailsAPI)

urlpatterns = [
    path(
        "merchant/disputes/<str:dispute_id>",
        MerchantDisputeDetailsAPI.as_view(),
        name="merchant_disputes_details",
    ),
    path(
        "merchant/disputes/",
        DisputeListAPI.as_view(),
        name="merchant_disputes_history",
    ),
    path(
        "consumer/dispute/create/",
        CreateDisputeAPI.as_view(),
        name="create_dispute",
    ),
    path(
        "consumer/dispute/reason-types/",
        DisputeReasonTypesAPI.as_view(),
        name="dispute_reason_types",
    ),
    path(
        "consumer/disputes/",
        ConsumerDisputeDetailsAPI.as_view(),
        name="consumer_dispute_details",
    ),
]
