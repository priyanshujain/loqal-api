from django.conf.urls import url

from apps.box.views.consumer import CreateFileAPI, FetchFileUrlAPI

urlpatterns = [
    url(
        r"^create/?$",
        CreateFileAPI.as_view(),
    ),
    url(
        r"^$",
        FetchFileUrlAPI.as_view(),
    ),
]
