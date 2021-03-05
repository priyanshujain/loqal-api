from .consumer import urlpatterns as consumer_urls
from .merchant import urlpatterns as merchant_urls

urlpatterns = merchant_urls + consumer_urls
