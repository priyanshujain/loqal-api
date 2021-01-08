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


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_INACTIVITY_EXPIRATION_DURATION = 600


NUM_PROXIES = 2