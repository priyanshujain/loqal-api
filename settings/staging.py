# coding=utf-8
import urllib

from apps.provider.options import APIEnvironmentTypes

DEBUG = False

ALLOWED_HOSTS = ["*"]


# vendor API env
API_ENV = APIEnvironmentTypes.SANDBOX
from .base import *  # isort:skip


CORS_ORIGIN_REGEX_WHITELIST += [
    "https://staff-stag.payloqal.com",
    "https://merchant-stag.payloqal.com",
    "https://website-stag.payloqal.com",
    "https://api-sandbox.dwolla.com",
]

APP_NAME = "Loqal"

# app config
APP_BASE_URL = "https://merchant-stag.payloqal.com"
API_BASE_URL = "https://api-stag.payloqal.com"
CONSUMER_APP_WEB_BASE_URL = "https://website-stag.payloqal.com"
MERCHANT_APP_WEB_BASE_URL = "https://merchant-stag.payloqal.com"

# Email configs.
DEFAULT_FROM_EMAIL = "hello@loqal.us"
EMAIL_SENDER_NAME = "Loqal Team"

CSRF_TRUSTED_ORIGINS = [
    "staff-stag.payloqal.com",
    "merchant-stag.payloqal.com",
    "website-stag.payloqal.com",
]


CELERY_BROKER_URL = "sqs://{0}:{1}@".format(
    urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=""),
    urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe=""),
)


CELERY_TASK_DEFAULT_QUEUE = env("CELERY_TASK_DEFAULT_QUEUE")

NUM_PROXIES = 2

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_INACTIVITY_EXPIRATION_DURATION = 600
SESSION_COOKIE_AGE = 86400

CSRF_COOKIE_SAMESITE = True
SESSION_COOKIE_SAMESITE = True


SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 2592000
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_SSL_REDIRECT = True

LOQAL_SMS_PHONE_NUMBER = "4122183340"
LOQAL_SMS_PHONE_NUMBER_COUNTRY = "US"
