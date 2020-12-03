from django.urls import path

from apps.payment.views import CreatePaymentAPI

urlpatterns = [
    path("create/", CreatePaymentAPI.as_view(), name="create_payment"),
]
