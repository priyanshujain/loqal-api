from .consumer import urlpatterns as consumer_urls
from .member import urlpatterns as member_urls
from .onboarding import urlpatterns as onboarding_urls
from .profile import urlpatterns as profile_urls
from .reference import urlpatterns as reference_urls

urlpatterns = (
    onboarding_urls
    + reference_urls
    + member_urls
    + profile_urls
    + consumer_urls
)
