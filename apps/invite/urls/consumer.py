from django.urls import path

from apps.invite.views.consumer import (DownloadAppAPI,
                                        FilterNonLoqalConsumersAPI)

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
]
