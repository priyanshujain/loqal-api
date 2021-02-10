from django.urls import path

from apps.core.views import AppMetaDataAPI, GetAppMetaDataAPI

urlpatterns = [
    path(
        "staff/app-metadata/",
        AppMetaDataAPI.as_view(),
        name="app_metadata",
    ),
    path(
        "app-metadata/",
        GetAppMetaDataAPI.as_view(),
        name="app_metadata_public",
    ),
]
