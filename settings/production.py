from apps.provider.options import APIEnvironmentTypes

from .staging import *  # isort:skip

DEBUG = False

ALLOWED_HOSTS = ["*"]


DOMAIN = env("DOMAIN")
CSRF_COOKIE_DOMAIN = DOMAIN
SESSION_COOKIE_DOMAIN = DOMAIN

SESSION_COOKIE_AGE = 43200  # half day


# vendor API env
API_ENV = APIEnvironmentTypes.PRODUCTION


CORS_ORIGIN_REGEX_WHITELIST += [
    "https://app.payloqal.com",
]


# app config
APP_BASE_URL = "https://merchant.payloqal.com"
API_BASE_URL = "https://api.payloqal.com"
CONSUMER_APP_WEB_BASE_URL = "https://payloqal.com"
MERCHANT_APP_WEB_BASE_URL = "https://merchant.payloqal.com"

# Email configs.
DEFAULT_FROM_EMAIL = "hello@payloqal.com"
EMAIL_SENDER_NAME = "Loqal App Team"


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_INACTIVITY_EXPIRATION_DURATION = 600


NUM_PROXIES = 2


SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 30
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"
