from apps.provider.options import APIEnvironmentTypes

DEBUG = True

ALLOWED_HOSTS = ["*"]


# vendor API env
API_ENV = APIEnvironmentTypes.DEMO
from .base import *  # isort:skip


CORS_ORIGIN_REGEX_WHITELIST += [
    "http://localhost:3000",
]


SESSION_INACTIVITY_EXPIRATION_DURATION = 86400

SPOTLIGHT_ADMIN_EMAIL = "test@spotlightandcompany.com"

APP_NAME = "Spotlight Local"
