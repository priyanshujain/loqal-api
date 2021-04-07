from django.urls import path

from apps.invite.views.consumer import (ConsumerInvitesAPI, DownloadAppAPI,
                                        FilterNonLoqalConsumersAPI,
                                        InviteConsumerAPI,
                                        ResendConsumerInviteAPI)

urlpatterns = [
    path(
        "consumer/download-app/",
        DownloadAppAPI.as_view(),
        name="consumer_download_app",
    ),
    path(
        "consumer/filter-nonloqal-phonenumbers/",
        FilterNonLoqalConsumersAPI.as_view(),
        name="filter_non_loqal_consumers",
    ),
    path(
        "consumer/invite/create/",
        InviteConsumerAPI.as_view(),
        name="invite_consumer",
    ),
    path(
        "consumer/invite/resend/",
        ResendConsumerInviteAPI.as_view(),
        name="resend_invite_api",
    ),
    path(
        "consumer/invites/",
        ConsumerInvitesAPI.as_view(),
        name="c2c_invites",
    ),
]
