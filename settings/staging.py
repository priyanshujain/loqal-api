# coding=utf-8
import os
from pathlib import Path

from apps.provider.options import APIEnvironmentTypes

DEBUG = False

ALLOWED_HOSTS = ["*"]


# vendor API env
API_ENV = APIEnvironmentTypes.DEMO
from .base import *  # isort:skip


CORS_ORIGIN_REGEX_WHITELIST += [
    "https://app-stag.payloqal.com",
]

APP_NAME = "Spotlight Staging"


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_INACTIVITY_EXPIRATION_DURATION = 600
