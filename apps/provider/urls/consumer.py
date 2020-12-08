from django.urls import path

from apps.provider.views.consumer import ListPaymentProviderAPI

urlpatterns = [
    path("", ListPaymentProviderAPI.as_view(),),
]
