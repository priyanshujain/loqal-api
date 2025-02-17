# coding=utf-8
from apps.provider.options import APIEnvironmentTypes

from .staging import *  # isort:skip


ALLOWED_HOSTS = ["*"]

# vendor API env
API_ENV = APIEnvironmentTypes.PRODUCTION

CORS_ORIGIN_WHITELIST = [
    "https://merchant.loqal.us",
    "https://api.dwolla.com",
    "https://loqal.us",
    "https://staff.loqal.us",
]

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

SESSION_COOKIE_DOMAIN = ".loqal.us"

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 20  # 15M
FILE_UPLOAD_MAX_MEMORY_SIZE = DATA_UPLOAD_MAX_MEMORY_SIZE
