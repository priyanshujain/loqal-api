from django.urls import path

from apps.account.views.staff import GetActiveMerchantsAPI

urlpatterns = [
    path(
        "staff/merchants/",
        GetActiveMerchantsAPI.as_view(),
        name="active_merchants",
    )
]
