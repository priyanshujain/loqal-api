from django.urls import path

from apps.banking.views.consumer import CreateBankAccountAPI

urlpatterns = [
    path("accounts/create/", CreateBankAccountAPI.as_view(),),
]
