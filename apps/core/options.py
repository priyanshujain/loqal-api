from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum


class PlatformTypes(ChoiceCharEnum):
    IOS = "ios", _("iOS")
    ANDROID = "android", _("Android")
    WEB = "web", _("Web")


class APIEnvironmentTypes(ChoiceCharEnum):
    PRODUCTION = "production", _("Production")
    STAGING = "staging", _("Staging")
    DEVELOPMENT = "development", _("Development")
