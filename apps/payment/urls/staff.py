from django.urls import path

from apps.payment.views.dispute import (ChangeDisputeStatusAPI,
                                        CloseDisputeAPI, GetAllDisputeAPI)

urlpatterns = [
    path(
        "staff/disputes/<str:dispute_id>/close/",
        CloseDisputeAPI.as_view(),
        name="close_dispute",
    ),
    path(
        "staff/disputes/<str:dispute_id>/update/",
        ChangeDisputeStatusAPI.as_view(),
        name="update_dispute",
    ),
    path(
        "staff/disputes/",
        GetAllDisputeAPI.as_view(),
        name="all_disputes",
    ),
]
