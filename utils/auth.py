from __future__ import absolute_import

import six

from django.conf import settings
from django.contrib.auth import login as _login
from django.contrib.auth import authenticate, logout
from time import time

from apps.user.models import User, Authenticator


MFA_SESSION_KEY = "mfa"


class AuthUserPasswordExpired(Exception):
    def __init__(self, user):
        self.user = user


def get_pending_2fa_user(request):
    rv = request.session.get("_pending_2fa")
    if rv is None:
        return

    user_id, created_at = rv[:2]
    if created_at < time() - 60 * 5:
        return None

    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        pass


def has_pending_2fa(request):
    return request.session.get("_pending_2fa") is not None



def login(request, user, passed_2fa=None, after_2fa=None, organization_id=None, source=None):
    """
    This logs a user in for the session and current request.

    If 2FA is enabled this method will start the MFA flow and return False as
    required.  If `passed_2fa` is set to `True` then the 2FA flow is set to be
    finalized (user passed the flow).

    If the session has already resolved MFA in the past, it will automatically
    detect it from the session.

    Optionally `after_2fa` can be set to a URL which will be used to override
    the regular session redirect target directly after the 2fa flow.

    Returns boolean indicating if the user was logged in.
    """
    has_2fa = Authenticator.objects.user_has_2fa(user)
    if passed_2fa is None:
        passed_2fa = request.session.get(MFA_SESSION_KEY, "") == six.text_type(user.id)

    if has_2fa and not passed_2fa:
        request.session["_pending_2fa"] = [user.id, time(), organization_id]
        if after_2fa is not None:
            request.session["_after_2fa"] = after_2fa
        request.session.modified = True
        return False

    # TODO(dcramer): this needs to be bound based on MFA options
    if passed_2fa:
        request.session[MFA_SESSION_KEY] = six.text_type(user.id)
        request.session.modified = True

    mfa_state = request.session.pop("_pending_2fa", ())
    if organization_id is None and len(mfa_state) == 3:
        organization_id = mfa_state[2]

    # Check for expired passwords here after we cleared the 2fa flow.
    # While this means that users will have to pass 2fa before they can
    # figure out that their passwords are expired this is still the more
    # reasonable behavior.
    #
    # We also remember _after_2fa here so that we can continue the flow if
    # someone does it in the same browser.
    if user.is_password_expired:
        raise AuthUserPasswordExpired(user)


    # If there is no authentication backend, just attach the first
    # one and hope it goes through.  This apparently is a thing we
    # have been doing for a long time, just moved it to a more
    # reasonable place.
    if not hasattr(user, "backend"):
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
    _login(request, user)
    return True

