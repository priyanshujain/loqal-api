from django.conf import settings
from django.conf.urls import handler403, handler404, handler500, include
from django.conf.urls.static import static
from django.urls import path

from apps.views import WelcomeAPI, error404

# handler404 = error404


urlpatterns = [
    path("api/user/", include("apps.user.urls.consumer")),
    path("api/account/", include("apps.account.urls")),
    path("api/banking/", include("apps.banking.urls")),
    path("api/box/", include("apps.box.urls.consumer")),
    path("api/payment/", include("apps.payment.urls")),
    path("api/merchant/", include("apps.merchant.urls")),
    path("api/provider/", include("apps.provider.urls.consumer")),
    path("api/staff/tracking/", include("apps.tracking.urls")),
    path("api/staff/provider/", include("apps.provider.urls.staff")),
    path("", WelcomeAPI.as_view()),
]
