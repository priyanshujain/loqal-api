from .onboarding import urlpatterns as onboarding_urls
from .reference import urlpatterns as reference_urls
from .member import urlpatterns as member_urls

urlpatterns = onboarding_urls + reference_urls + member_urls