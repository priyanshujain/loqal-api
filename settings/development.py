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
    "https://app-dev.payloqal.com",
    "https://merchant-demo.payloqal.com",
    "https://dev-website.payloqal.com",
]


SESSION_INACTIVITY_EXPIRATION_DURATION = 86400

SPOTLIGHT_ADMIN_EMAIL = "test@spotlightandcompany.com"


CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"

SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

SESSION_INACTIVITY_EXPIRATION_DURATION = 86400
