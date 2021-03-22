from django.urls import path

from apps.box.views.consumer import CreateFileAPI, FetchFileUrlAPI

urlpatterns = [
    path(
        "create/",
        CreateFileAPI.as_view(),
        name="create_boxfile",
    ),
    path(
        "",
        FetchFileUrlAPI.as_view(),
        name="get_boxfile_url",
    ),
]
