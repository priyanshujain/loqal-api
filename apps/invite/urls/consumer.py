from django.urls import path

from apps.invite.views.consumer import DownloadAppAPI

urlpatterns = [
    path(
        "consumer/download-app/",
        DownloadAppAPI.as_view(),
        name="consumer_download_app",
    ),
]
