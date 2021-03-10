from django.urls import path

from apps.merchant.views.invite import InviteConsumerAPI

urlpatterns = [
    path(
        "invite/consumer/",
        InviteConsumerAPI.as_view(),
        name="invite_consumer",
    )
]
