import re
from datetime import timedelta

from django.utils.timezone import now

from apps.user.models import User, UserPasswordReset, UserSession
from utils.shortcuts import rand_str

__all__ = (
    "create_user",
    "update_user_profile",
    "get_user_by_email",
    "create_session",
    "get_active_sessions",
    "get_all_sessions",
    "get_session",
    "set_new_user_password",
    "gen_reset_password_token",
    "get_reset_password_object_by_token",
    "get_user_by_email_token",
    "get_user_by_phone",
)


def create_user(
    first_name,
    last_name,
    email,
    password,
    phone_number=None,
    email_verified=False,
):
    user = User.objects.create(
        username=email,
        email=email,
        email_verified=email_verified,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
    )
    user.set_password(password)
    user.gen_email_verification_token()
    return user


def update_user_profile(user, first_name, last_name):
    """
    User user profile dbapi
    """
    user.first_name = first_name
    user.last_name = last_name
    user.save()


def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def create_session(
    user_id,
    session_key,
    user_agent,
    ip_address,
    is_ip_routable,
    last_activity,
    ip_country_iso,
    country_iso,
    region,
    region_code,
    latitude,
    longitude,
    timezone,
    asn,
    asn_code,
):
    return UserSession.objects.create(
        user_id=user_id,
        session_key=session_key,
        user_agent=user_agent,
        ip_address=ip_address,
        is_ip_routable=is_ip_routable,
        last_activity=last_activity,
        ip_country_iso=ip_country_iso,
        country_iso=country_iso,
        region=region,
        region_code=region_code,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        asn=asn,
        asn_code=asn_code,
    )


def get_active_sessions(user_id):
    return UserSession.objects.filter(user_id=user_id, is_expired=False)


def get_all_sessions(user_id):
    return UserSession.objects.filter(user_id=user_id)


def get_session(user_id, session_key):
    """
    current session
    """
    try:
        return UserSession.objects.get(
            user_id=user_id, is_expired=False, session_key=session_key
        )
    except UserSession.DoesNotExist:
        return None


def set_new_user_password(user, new_password):
    user.set_password(new_password)
    user.save()


def gen_reset_password_token(user_id):
    token = rand_str()
    token_expire_time = now() + timedelta(hours=24)
    return UserPasswordReset.objects.create(
        user_id=user_id,
        token=token,
        token_expire_time=token_expire_time,
    )


def get_reset_password_object_by_token(token):
    qs = UserPasswordReset.objects.filter(token=token)
    if qs.exists():
        return qs.first()
    return None


def get_user_by_email_token(token):
    qs = User.objects.filter(email_verification_token=token)
    if qs.exists():
        return qs.first()
    return None


def get_user_by_phone(phone_number):
    user_qs = User.objects.filter(phone_number=phone_number)
    if user_qs.exists():
        return user_qs.first()
    return None
