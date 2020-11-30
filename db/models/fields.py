# Python
import logging
import re
import urllib.parse as urlparse

# Django
from django.core.validators import URLValidator, _lazy_re_compile
from django.utils.translation import ugettext_lazy as _
# Django REST Framework
from rest_framework.fields import (BooleanField, CharField, ChoiceField,
                                   DateTimeField, DictField, EmailField,
                                   IntegerField, ListField)

logger = logging.getLogger("db.models.fields")

# Use DRF fields to convert/validate settings:
# - to_representation(obj) should convert a native Python object to a primitive
#   serializable type. This primitive type will be what is presented in the API
#   and stored in the JSON field in the datbase.
# - to_internal_value(data) should convert the primitive type back into the
#   appropriate Python type to be used in settings.


class BooleanField(BooleanField):
    pass


class ChoiceField(ChoiceField):
    pass


class DateTimeField(DateTimeField):
    pass


class DictField(DictField):
    pass


class EmailField(EmailField):
    pass


class ListField(ListField):
    pass


class CharField(CharField):
    def to_representation(self, value):
        # django_rest_frameworks' default CharField implementation casts `None`
        # to a string `"None"`:
        #
        # https://github.com/tomchristie/django-rest-framework/blob/cbad236f6d817d992873cd4df6527d46ab243ed1/rest_framework/fields.py#L761
        if value is None:
            return None
        return super(CharField, self).to_representation(value)


class IntegerField(IntegerField):
    def get_value(self, dictionary):
        ret = super(IntegerField, self).get_value(dictionary)
        # Handle UI corner case
        if (
            ret == ""
            and self.allow_null
            and not getattr(self, "allow_blank", False)
        ):
            return None
        return ret


class StringListField(ListField):

    child = CharField()

    def to_representation(self, value):
        if value is None and self.allow_null:
            return None
        return super(StringListField, self).to_representation(value)


class URLField(CharField):
    # these lines set up a custom regex that allow numbers in the
    # top-level domain
    tld_re = (
        r"\."  # dot
        r"(?!-)"  # can't start with a dash
        r"(?:[a-z"
        + URLValidator.ul
        + r"0-9"
        + "-]{2,63}"  # domain label, this line was changed from the original URLValidator
        r"|xn--[a-z0-9]{1,59})"  # or punycode label
        r"(?<!-)"  # can't end with a dash
        r"\.?"  # may have a trailing dot
    )

    host_re = (
        "("
        + URLValidator.hostname_re
        + URLValidator.domain_re
        + tld_re
        + "|localhost)"
    )

    regex = _lazy_re_compile(
        r"^(?:[a-z0-9\.\-\+]*)://"  # scheme is validated separately
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:"
        + URLValidator.ipv4_re
        + "|"
        + URLValidator.ipv6_re
        + "|"
        + host_re
        + ")"
        r"(?::\d{2,5})?"  # port
        r"(?:[/?#][^\s]*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )

    def __init__(self, **kwargs):
        schemes = kwargs.pop("schemes", None)
        regex = kwargs.pop("regex", None)
        self.allow_plain_hostname = kwargs.pop("allow_plain_hostname", False)
        self.allow_numbers_in_top_level_domain = kwargs.pop(
            "allow_numbers_in_top_level_domain", True
        )
        super(URLField, self).__init__(**kwargs)
        validator_kwargs = dict(message=_("Enter a valid URL"))
        if schemes is not None:
            validator_kwargs["schemes"] = schemes
        if regex is not None:
            validator_kwargs["regex"] = regex
        if self.allow_numbers_in_top_level_domain and regex is None:
            # default behavior is to allow numbers in the top level domain
            # if a custom regex isn't provided
            validator_kwargs["regex"] = URLField.regex
        self.validators.append(URLValidator(**validator_kwargs))

    def to_representation(self, value):
        if value is None:
            return ""
        return super(URLField, self).to_representation(value)

    def run_validators(self, value):
        if self.allow_plain_hostname:
            try:
                url_parts = urlparse.urlsplit(value)
                if url_parts.hostname and "." not in url_parts.hostname:
                    netloc = "{}.local".format(url_parts.hostname)
                    if url_parts.port:
                        netloc = "{}:{}".format(netloc, url_parts.port)
                    if url_parts.username:
                        if url_parts.password:
                            netloc = "{}:{}@{}".format(
                                url_parts.username, url_parts.password, netloc
                            )
                        else:
                            netloc = "{}@{}".format(url_parts.username, netloc)
                    value = urlparse.urlunsplit(
                        [
                            url_parts.scheme,
                            netloc,
                            url_parts.path,
                            url_parts.query,
                            url_parts.fragment,
                        ]
                    )
            except Exception:
                raise  # If something fails here, just fall through and let the validators check it.
        super(URLField, self).run_validators(value)
