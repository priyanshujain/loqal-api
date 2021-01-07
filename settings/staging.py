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
    "https://app-stag.payloqal.com",
]

APP_NAME = "Loqal staging"


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
