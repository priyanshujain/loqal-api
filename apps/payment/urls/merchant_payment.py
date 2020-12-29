from django.urls import path

from apps.payment.views.merchant_payment import MerchantPaymentDetailsAPI,MerchantCustomersAPI, MerchantCustomerDetailsAPI

urlpatterns = [
    path(
        "details/<str:payment_id>/",
        MerchantPaymentDetailsAPI.as_view(),
        name="merchant_payment_details",
    ),
    path(
        "merchant/customers/",
        MerchantCustomersAPI.as_view(),
        name="merchant_customers",
    ),
    path(
        "merchant/customers/<str:customer_id>/",
        MerchantCustomerDetailsAPI.as_view(),
        name="merchant_customer_details",
    ),
]
