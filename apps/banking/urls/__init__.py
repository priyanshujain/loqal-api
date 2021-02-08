from .consumer import urlpatterns as consumer_urls
from .merchant import urlpatterns as merchant_urls
from .sandbox import urlpatterns as sandbox_urls

urlpatterns = consumer_urls + merchant_urls + sandbox_urls
