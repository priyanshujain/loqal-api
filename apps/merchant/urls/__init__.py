from .consumer import urlpatterns as consumer_urls
from .invite import urlpatterns as invite_urls
from .member import urlpatterns as member_urls
from .member_staff import urlpatterns as member_staff_urls
from .member_user import urlpatterns as member_user_urls
from .onboarding import urlpatterns as onboarding_urls
from .pos import urlpatterns as pos_urls
from .profile import urlpatterns as profile_urls
from .reference import urlpatterns as reference_urls

urlpatterns = (
    onboarding_urls
    + reference_urls
    + member_urls
    + profile_urls
    + consumer_urls
    + member_user_urls
    + member_staff_urls
    + invite_urls
    + pos_urls
)
