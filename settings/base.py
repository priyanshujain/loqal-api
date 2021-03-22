import os

import django_opentracing
import environ
import sentry_sdk
from corsheaders.defaults import default_headers
from cryptography.fernet import Fernet
from django.utils.encoding import smart_bytes
from google.oauth2 import service_account
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

DEBUG = True

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path("apps")
DATA_DIR = f"{ROOT_DIR}/data"

env = environ.Env()
env.read_env(str(ROOT_DIR.path(".env")))

APP_ENV = env("APP_ENV")

allow_sentry_logging = False
if not APP_ENV in ["development", "local"]:
    allow_sentry_logging = True

SECRET_KEY = env("SECRET_KEY")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Applications

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]
VENDOR_APPS = [
    "rest_framework",
    "django_extensions",
    "django_dbconn_retry",
    "corsheaders",
    "versatileimagefield",
]


LOCAL_APPS = [
    "apps.user",
    "apps.account",
    "apps.tracking",
    "apps.provider",
    "apps.box",
    "apps.banking",
    "apps.payment",
    "apps.merchant",
    "apps.reference",
    "apps.order",
    "apps.notification",
    "apps.support",
    "apps.metrics",
    "apps.marketing",
    "apps.core",
    "apps.reward",
    "apps.invite",
]

INSTALLED_APPS = DJANGO_APPS + VENDOR_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django_opentracing.OpenTracingMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_feature_policy.PermissionsPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "config.middlewares.AddXCsrfMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middlewares.SessionRecordMiddleware",
    "config.middlewares.LocalUserMiddleware",
    "config.middlewares.PreventAuthenticatePromptMiddleware",
    # "config.middlewares.AdminRoleRequiredMiddleware",
    # 'config.middlewares.LogSqlMiddleware',
]


ROOT_URLCONF = "apps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "lib.auth.password_validation.ContainsUppercaseValidator",
    },
    {
        "NAME": "lib.auth.password_validation.ContainsLowercaseValidator",
    },
    {
        "NAME": "lib.auth.password_validation.ContainsSpecialCharactersValidator",
    },
    {"NAME": "lib.auth.password_validation.ContainsDigitsValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "data/static/")
STATIC_URL = "/static/"

AUTH_USER_MODEL = "user.User"

TEST_CASE_DIR = os.path.join(DATA_DIR, "test_case")
LOG_PATH = os.path.join(DATA_DIR, "log")

AVATAR_URI_PREFIX = "/public/avatar"
AVATAR_UPLOAD_DIR = f"{DATA_DIR}{AVATAR_URI_PREFIX}"

UPLOAD_PREFIX = "/public/upload"
UPLOAD_DIR = f"{DATA_DIR}{UPLOAD_PREFIX}"

STATICFILES_DIRS = [os.path.join(DATA_DIR, "public")]


# Sentry config

# TODO: strip_sensitive_data before sending
# https://docs.sentry.io/platforms/python/configuration/filtering/
sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration(), RedisIntegration()],
    _experiments={"auto_enabling_integrations": True},
    # FIX: Frontend is giving no internet if applied invalid value of sample_rate
    # traces_sample_rate=env("TRACES_SAMPLE_RATE"),
    environment=env("APP_ENV"),
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)


LOGGING_HANDLERS = (
    ["console", "sentry"] if allow_sentry_logging else ["console"]
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] - [%(levelname)s] - [%(name)s:%(lineno)d]  - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "sentry": {
            "level": "ERROR",
            "class": "sentry_sdk.integrations.logging.EventHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": LOGGING_HANDLERS,
            "level": "ERROR",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": LOGGING_HANDLERS,
            "level": "ERROR",
            "propagate": True,
        },
        "celery": {
            "handlers": LOGGING_HANDLERS,
            "level": "INFO",
            "propagate": True,
        },
        "": {
            "handlers": LOGGING_HANDLERS,
            "level": "WARNING",
            "propagate": True,
        },
    },
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_THROTTLE_CLASSES": [
        "api.throttling.UserBurstRateThrottle",
        "api.throttling.UserSustainedRateThrottle",
        "api.throttling.AnonBurstRateThrottle",
        "api.throttling.AnonSustainedRateThrottle",
        "api.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user_burst": "60/min",
        "user_sustained": "1000/day",
        "anon_burst": "20/min",
        "anon_sustained": "100/day",
        "login": "10/min",
    },
    "NON_FIELD_ERRORS_KEY": "detail",
}


# Database config
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
    }
}


# Cache config
REDIS_CONF = {"host": env("REDIS_HOST"), "port": env("REDIS_PORT")}
REDIS_URL = "redis://%s:%s" % (REDIS_CONF["host"], REDIS_CONF["port"])


def redis_config(db):
    def make_key(key, key_prefix, version):
        return key

    return {
        "BACKEND": "utils.cache.MyRedisCache",
        "LOCATION": f"{REDIS_URL}/{db}",
        "TIMEOUT": None,
        "KEY_PREFIX": "",
        "KEY_FUNCTION": make_key,
    }


CACHES = {"default": redis_config(db=1)}


# CSRF_COOKIE_NAME = "lc"

# TODO: look into it
# SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
# SESSION_CACHE_ALIAS = "default"
# SESSION_COOKIE_NAME = "session"

# # FIX: Change this to json serializer and convert last_activity to timestamp
# SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"


SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_NAME = "session"

# # FIX: Change this to json serializer and convert last_activity to timestamp
# SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"


# Celery config
CELERY_BROKER_URL = REDIS_URL
# RESULT_BACKEND = REDIS_URL
# ACCEPT_CONTENT = ["application/json"]
# TASK_SERIALIZER = "json"
# RESULT_SERIALIZER = "json"
# TIMEZONE = "UTC"
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 60

CELERY_ROUTES = {
    "apps.provider.services.process_webhook.tasks.process_webhook_event": {
        "queue": "psp_webhook"
    },
}


CORS_ORIGIN_REGEX_WHITELIST = []

# CORS_ORIGIN_ALLOW_ALL = True


CORS_EXPOSE_HEADERS = list(default_headers) + [
    "x-total",
    "x-api-time",
]

CORS_ALLOW_CREDENTIALS = True


DJANGO_SETTINGS_MODULE = "settings"


# OpenTracing settings

# if not included, defaults to True.
# has to come before OPENTRACING_TRACING setting because python...
OPENTRACING_TRACE_ALL = True

# defaults to []
# only valid if OPENTRACING_TRACE_ALL == True
OPENTRACING_TRACED_ATTRIBUTES = ["path", "method"]

# Callable that returns an `opentracing.Tracer` implementation.
OPENTRACING_TRACER_CALLABLE = "opentracing.Tracer"


# Email configs.
SENDGRID_API_KEY = env("SENDGRID_API_KEY")


# s3 config
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# AWS config
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# TODO: https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html


# Plaid config
PLAID_CLIENT_ID = env("PLAID_CLIENT_ID")
PLAID_ENV = env("PLAID_ENV")
PLAID_PUBLIC_KEY = env("PLAID_PUBLIC_KEY")
PLAID_SECRET = env("PLAID_SECRET")
PLAID_APP_NAME = "Loqal"
PLAID_PRODUCTS = [
    "auth",
    "balance",
]


PROXY_IP_ALLOWED_LIST = []
REMOTE_HOST_HEADERS = {}


SESSION_INACTIVITY_EXPIRATION_DURATION = 600


# Admin config
SPOTLIGHT_ADMIN_EMAIL = env("SPOTLIGHT_ADMIN_EMAIL")


MANAGERS = (("Priyanshu Jain", "priyanshu@spotlightandcompany.com"),)
ADMINS = MANAGERS

APP_NAME = env("APP_NAME", default="Loqal")


USE_CUSTOM_BIG_INTS = False


# Loqal Encryption
LOQAL_ENCRYPTION_KEY = env("LOQAL_ENCRYPTION_KEY")
LOQAL_ENCRYPTION_SCHEMES = (
    ("fernet", Fernet(smart_bytes(LOQAL_ENCRYPTION_KEY))),
)


# Max file size for avatar photo uploads
MAX_AVATAR_SIZE = 5000000


# Transaction settings
MIN_BANK_ACCOUNT_BALANCE_REQUIRED = 100.00
DEFAULT_MAX_DIGITS = 6
DEFAULT_DECIMAL_PLACES = 2


# Firebase settings
FCM_SERVER_KEY = env("FCM_SERVER_KEY")
FCM_SERVER = "https://fcm.googleapis.com/fcm/send"


# SMS config
LOQAL_SMS_PHONE_NUMBER = "4122183340"
LOQAL_SMS_PHONE_NUMBER_COUNTRY = "US"
DEFAULT_PHONE_REGION = "US"
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")

# Setup
INITIAL_ADMIN_PASSWORD = env("INITIAL_ADMIN_PASSWORD")

# Email configs.
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_SENDER_NAME = env("EMAIL_SENDER_NAME")

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "stores": [
        ("store_gallery", "thumbnail__540x540"),
        ("store_gallery_2x", "thumbnail__1080x1080"),
        ("store_small", "thumbnail__60x60"),
        ("store_small_2x", "thumbnail__120x120"),
        ("store_list", "thumbnail__255x255"),
        ("store_list_2x", "thumbnail__510x510"),
    ],
    "user_avatars": [
        ("default", "thumbnail__445x445"),
        ("small", "thumbnail__255x255"),
    ],
}

VERSATILEIMAGEFIELD_SETTINGS = {
    # Images should be pre-generated on Production environment
    # "create_images_on_demand": env("CREATE_IMAGES_ON_DEMAND")
    "create_images_on_demand": False
}


DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 50
