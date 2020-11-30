from django.conf import settings
from django.conf.urls import handler403, handler404, handler500, include
from django.conf.urls.static import static
from django.urls import path

from apps.views import WelcomeAPI, error404

# handler404 = error404


urlpatterns = [
    path("api/user/", include("apps.user.urls.consumer")),
    path("api/account/", include("apps.account.urls.consumer")),
    path("api/staff/tracking/", include("apps.tracking.urls")),
    path("", WelcomeAPI.as_view()),
]
