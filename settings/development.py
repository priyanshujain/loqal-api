# coding=utf-8
import os
from pathlib import Path

from apps.provider.options import APIEnvironmentTypes

DEBUG = False

ALLOWED_HOSTS = ["*"]


# vendor API env
API_ENV = APIEnvironmentTypes.SANDBOX
from .base import *  # isort:skip

APP_NAME = "Loqal development"


CORS_ORIGIN_REGEX_WHITELIST += [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://staff-dev.payloqal.com",
    "https://merchant-dev.payloqal.com",
    "https://website-dev.payloqal.com",
]


CSRF_TRUSTED_ORIGINS = [
    "staff-dev.payloqal.com",
    "merchant-dev.payloqal.com",
    "website-dev.payloqal.com",
]


SESSION_INACTIVITY_EXPIRATION_DURATION = 86400

SPOTLIGHT_ADMIN_EMAIL = "priyanshu@spotlightandcompany.com"


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_AGE = 86400

CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"


SESSION_COOKIE_NAME = '__Secure-sessionid'
CSRF_COOKIE_NAME = '__Secure-csrftoken'


SESSION_COOKIE_DOMAIN=".payloqal.com"



SESSION_INACTIVITY_EXPIRATION_DURATION = 86400

NUM_PROXIES = 2


# app config
APP_BASE_URL = "https://merchant-dev.payloqal.com"
API_BASE_URL = "https://api-dev.payloqal.com"
CONSUMER_APP_WEB_BASE_URL = "https://website-dev.payloqal.com"
MERCHANT_APP_WEB_BASE_URL = "https://merchant-dev.payloqal.com"

# Email configs.
DEFAULT_FROM_EMAIL = "donotreply@spotlightandcompany.com"
EMAIL_SENDER_NAME = "Loqal App Team"


SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 2592000
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"