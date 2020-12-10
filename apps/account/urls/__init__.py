from .merchant import urlpatterns as merchant_urls
from .consumer import urlpatterns as consumer_urls

urlpatterns = merchant_urls + consumer_urls