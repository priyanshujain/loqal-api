from django.conf import settings
from django.conf.urls import handler403, handler404, handler500, include
from django.conf.urls.static import static
from django.urls import path

from apps.views import WelcomeAPI, error404

# handler404 = error404


urlpatterns = [
    path("api/user/", include("apps.user.urls")),
    path("api/notification/", include("apps.notification.urls")),
    path("api/account/", include("apps.account.urls")),
    path("api/order/", include("apps.order.urls")),
    path("api/banking/", include("apps.banking.urls")),
    path("api/box/", include("apps.box.urls.consumer")),
    path("api/payment/", include("apps.payment.urls")),
    path("api/reference/", include("apps.reference.urls")),
    path("api/merchant/", include("apps.merchant.urls")),
    path("api/provider/", include("apps.provider.urls.consumer")),
    path("api/support/", include("apps.support.urls")),
    path("api/metrics/", include("apps.metrics.urls")),
    path("api/marketing/", include("apps.marketing.urls")),
    path("api/core/", include("apps.core.urls")),
    path("api/rewards/", include("apps.reward.urls")),
    path("api/invite/", include("apps.invite.urls")),
    path("api/staff/merchant/", include("apps.merchant.urls.staff")),
    path("api/staff/tracking/", include("apps.tracking.urls")),
    path("api/staff/provider/", include("apps.provider.urls.staff")),
    path("api/external/provider/", include("apps.provider.urls.external")),
    path("", WelcomeAPI.as_view()),
]
