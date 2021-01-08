# coding=utf-8
import os
import urllib
from pathlib import Path

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
]

APP_NAME = "Loqal staging"


# app config
APP_BASE_URL = "https://merchant-dev.payloqal.com"
API_BASE_URL = "https://api-dev.payloqal.com"
CONSUMER_APP_WEB_BASE_URL = "https://website-dev.payloqal.com"
MERCHANT_APP_WEB_BASE_URL = "https://merchant-dev.payloqal.com"

# Email configs.
DEFAULT_FROM_EMAIL = "hello@payloqal.com"
EMAIL_SENDER_NAME = "Loqal App Team"

CSRF_TRUSTED_ORIGINS = [
    "https://staff-stag.payloqal.com",
    "https://merchant-stag.payloqal.com",
    "https://website-stag.payloqal.com",
]

SESSION_COOKIE_DOMAIN=".payloqal.com"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_INACTIVITY_EXPIRATION_DURATION = 600


CELERY_BROKER_URL = "sqs://{0}:{1}@".format(
    urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=""),
    urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe=""),
)


CELERY_TASK_DEFAULT_QUEUE = env("AWS_SECRET_ACCESS_KEY")

NUM_PROXIES = 2

SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 30
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"
