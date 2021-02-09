# coding=utf-8
from apps.provider.options import APIEnvironmentTypes

from .staging import *  # isort:skip


ALLOWED_HOSTS = ["*"]

# vendor API env
API_ENV = APIEnvironmentTypes.PRODUCTION

CORS_ORIGIN_REGEX_WHITELIST += [
    "https://merchant.loqal.us",
    "https://api.dwolla.com",
    "https://loqal.us",
    "https://staff.loqal.us",
]

# app config
APP_BASE_URL = "https://merchant.loqal.us"
API_BASE_URL = "https://api.loqal.us"
CONSUMER_APP_WEB_BASE_URL = "https://loqal.us"
MERCHANT_APP_WEB_BASE_URL = "https://merchant.loqal.us"

# Email configs.
DEFAULT_FROM_EMAIL = "hello@loqal.us"
EMAIL_SENDER_NAME = "Loqal Team"
