from django.urls import path

from apps.merchant.views.invite import InviteConsumerAPI, InvitePosConsumerAPI

urlpatterns = [
    path(
        "invite/consumer/",
        InviteConsumerAPI.as_view(),
        name="invite_consumer",
    ),
    path(
        "pos/invite/consumer/",
        InvitePosConsumerAPI.as_view(),
        name="pos_invite_consumer",
    ),
]
