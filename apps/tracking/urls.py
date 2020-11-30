from django.urls import path

from apps.tracking.views import (PspRequestAPIView, PspRequestDetailsAPIView,
                                 PspRequestErrorsAPIView)

urlpatterns = [
    path("errors/<int:account_id>/", PspRequestErrorsAPIView.as_view(),),
    path(
        "<int:account_id>/requests/<int:request_id>/details/",
        PspRequestDetailsAPIView.as_view(),
    ),
    path("<int:account_id>/", PspRequestAPIView.as_view(),),
]
