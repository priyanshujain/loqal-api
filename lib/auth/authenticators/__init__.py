from __future__ import absolute_import

import six

from .base import AuthenticatorInterface  # NOQA
from .sms import SmsInterface
from .totp import TotpInterface

AUTHENTICATOR_INTERFACES = {}
AUTHENTICATOR_INTERFACES_BY_TYPE = {}
AUTHENTICATOR_CHOICES = []


def register_authenticator(cls):
    AUTHENTICATOR_INTERFACES[cls.interface_id] = cls
    AUTHENTICATOR_INTERFACES_BY_TYPE[cls.type] = cls
    AUTHENTICATOR_CHOICES.append((cls.type, cls.name))
    AUTHENTICATOR_CHOICES.sort(key=lambda x: x[0])


def available_authenticators(ignore_backup=False):
    interfaces = six.itervalues(AUTHENTICATOR_INTERFACES)
    if not ignore_backup:
        return [v for v in interfaces if v.is_available]
    return [
        v for v in interfaces if not v.is_backup_interface and v.is_available
    ]


register_authenticator(SmsInterface)
register_authenticator(TotpInterface)
