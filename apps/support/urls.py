from django.urls import path

from apps.support.views import SupportRequestAPI, SupportRequestHistoryAPI

urlpatterns = [
    path(
        "ticket/history/",
        SupportRequestHistoryAPI.as_view(),
        name="support_request_history",
    ),
    path(
        "ticket/", SupportRequestAPI.as_view(), name="create_support_request"
    ),
]
