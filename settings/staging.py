# coding=utf-8
import urllib

from apps.provider.options import APIEnvironmentTypes

from .development import *  # isort:skip


CORS_ORIGIN_REGEX_WHITELIST += [
    "https://staff-stag.payloqal.com",
    "https://merchant-stag.payloqal.com",
    "https://website-stag.payloqal.com",
    "https://api-sandbox.dwolla.com",
]


# app config
APP_BASE_URL = "https://merchant-stag.payloqal.com"
API_BASE_URL = "https://api-stag.payloqal.com"
CONSUMER_APP_WEB_BASE_URL = "https://website-stag.payloqal.com"
MERCHANT_APP_WEB_BASE_URL = "https://merchant-stag.payloqal.com"


CELERY_BROKER_URL = "sqs://{0}:{1}@".format(
    urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=""),
    urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe=""),
)
CELERY_TASK_DEFAULT_QUEUE = env("CELERY_TASK_DEFAULT_QUEUE")

CSRF_COOKIE_NAME = '__Secure-csrftoken'
CSRF_COOKIE_SAMESITE = True
SESSION_COOKIE_SAMESITE = True


REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "user_burst": "60/min",
    "user_sustained": "1000/day",
    "anon_burst": "20/min",
    "anon_sustained": "100/day",
    "login": "10/min",
}
