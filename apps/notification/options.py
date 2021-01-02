from django.utils.translation import gettext as _

from db.models.fields import ChoiceCharEnum


class UserDeviceTypes(ChoiceCharEnum):
    IOS = "ios", _("iOS")
    ANDROID = "android", _("Android")
    WEB = "web", _("Web")
