from apps.provider.options import APIEnvironmentTypes

DEBUG = True

ALLOWED_HOSTS = ["*"]


# vendor API env
API_ENV = APIEnvironmentTypes.SANDBOX
from .base import *  # isort:skip


CORS_ORIGIN_REGEX_WHITELIST += [
    "http://localhost:3000",
]


SESSION_INACTIVITY_EXPIRATION_DURATION = 86400

SPOTLIGHT_ADMIN_EMAIL = "test@spotlightandcompany.com"

APP_NAME = "Loqal local"


# app config
APP_BASE_URL = "http://localhost:3000"
API_BASE_URL = "http://localhost:8000"
CONSUMER_APP_WEB_BASE_URL = "http://localhost:3001"
MERCHANT_APP_WEB_BASE_URL = "http://localhost:3001"

# Email configs.
DEFAULT_FROM_EMAIL = "donotreply@spotlightandcompany.com"
EMAIL_SENDER_NAME = "Loqal App Team"


LOQAL_SMS_PHONE_NUMBER = "4122183340"
LOQAL_SMS_PHONE_NUMBER_COUNTRY = "US"
