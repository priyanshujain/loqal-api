import os

import django_opentracing
import environ
import sentry_sdk
from corsheaders.defaults import default_headers
from google.oauth2 import service_account
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

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
]


LOCAL_APPS = [
    "apps.user",
    "apps.account",
    "apps.tracking",
    "apps.provider",
    "apps.box",
    "apps.banking",
]

INSTALLED_APPS = DJANGO_APPS + VENDOR_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django_opentracing.OpenTracingMiddleware",
    "django.middleware.security.SecurityMiddleware",
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
            "level": "DEBUG",
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

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Celery config
CELERY_BROKER_URL = REDIS_URL
# RESULT_BACKEND = REDIS_URL
# ACCEPT_CONTENT = ["application/json"]
# TASK_SERIALIZER = "json"
# RESULT_SERIALIZER = "json"
# TIMEZONE = "UTC"


CORS_ORIGIN_REGEX_WHITELIST = []

# CORS_ORIGIN_ALLOW_ALL = True


CORS_EXPOSE_HEADERS = list(default_headers) + [
    "x-total",
    "x-api-time",
]

CORS_ALLOW_CREDENTIALS = True


# Cloud storage configs.
GS_CREDENTIAL_PATH = os.path.join(DATA_DIR, "config/credentials.json")
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    GS_CREDENTIAL_PATH
)

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


# app config
APP_BASE_URL = env("APP_BASE_URL")
API_BASE_URL = env("API_BASE_URL")


# Email configs.
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_SENDER_NAME = env("EMAIL_SENDER_NAME")
SENDGRID_API_KEY = env("SENDGRID_API_KEY")


# GCS config
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"


# Plaid config
PLAID_CLIENT_ID = env("PLAID_CLIENT_ID")
PLAID_ENV = env("PLAID_ENV")
PLAID_PUBLIC_KEY = env("PLAID_PUBLIC_KEY")
PLAID_SECRET = env("PLAID_SECRET")


PROXY_IP_ALLOWED_LIST = []
REMOTE_HOST_HEADERS = {}


SESSION_INACTIVITY_EXPIRATION_DURATION = 600


# Admin config
SPOTLIGHT_ADMIN_EMAIL = env("SPOTLIGHT_ADMIN_EMAIL")


MANAGERS = (("Priyanshu Jain", "priyanshu@spotlightandcompany.com"),)
ADMINS = MANAGERS

APP_NAME = env("APP_NAME", default="Spotlight")
