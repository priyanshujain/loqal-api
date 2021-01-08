"""
1. List session
2. Delete session
"""
from importlib import import_module

from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from apps.user.dbapi import create_session as _create_session
from apps.user.dbapi import (get_active_sessions, get_all_sessions,
                             get_session_by_id)

__all__ = ("Session",)


class Session(object):
    def __init__(self, request, only_active=False):
        self.request = request
        self.only_active = only_active
        self.user = request.user

    def create_session(self, user):
        """
        Create session record
        """
        # TODO: Combine cache based session and models based session so that
        #       we have a record of expired sessions.
        session = self.request.session

        # TODO: get ifconfig from IP address, need to implment maxmind geodb service
        ifconfig = {}
        # from cache based session
        user_agent = session["user_agent"]
        ip_address = session["ip"]
        is_ip_routable = session["is_ip_routable"]
        last_activity = session["last_activity"]
        ip_country_iso = session["cf_ip_country"]

        # from maxmind ifconfig
        country_iso = ifconfig.get("country_iso", "")
        region = ifconfig.get("region", "")
        region_code = ifconfig.get("region_code", "")
        latitude = ifconfig.get("latitude", "")
        longitude = ifconfig.get("longitude", "")
        timezone = ifconfig.get("timezone", "")
        asn = ifconfig.get("asn_org", "")
        asn_code = ifconfig.get("asn", "")

        _create_session(
            user_id=user.id,
            session_key=session.session_key,
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

    def list_sessions(self):
        # FIX: current session is causing error it's always showing false
        user = self.user
        request_session = self.request.session

        if self.only_active:
            sessions = get_active_sessions(user_id=user.id)
        else:
            sessions = get_all_sessions(user_id=user.id)

        sessions_data = []
        for local_session in sessions:
            # session does not exist or is expired
            if not self.check_session_exists(
                session_key=local_session.session_key
            ):
                local_session.expire_session()
                if self.only_active:
                    continue
            sessions_data.append(
                {
                    "is_current_session": request_session.session_key
                    == local_session.session_key,
                    "session_id": local_session.id,
                    "user_agent": local_session.user_agent,
                    "ip_address": local_session.ip_address,
                    "is_ip_routable": local_session.is_ip_routable,
                    "last_activity": local_session.last_activity,
                    "ip_country_iso": local_session.ip_country_iso,
                    "country_iso": local_session.country_iso,
                    "region": local_session.region,
                    "region_code": local_session.country_iso,
                    "latitude": local_session.latitude,
                    "longitude": local_session.longitude,
                    "asn": local_session.asn,
                    "is_expired": local_session.is_expired,
                }
            )
        return sessions_data

    def check_session_exists(self, session_key):
        engine = import_module(settings.SESSION_ENGINE)
        session_store = engine.SessionStore
        session = session_store(session_key)
        if session._session:
            return True
        return False

    def delete_session(self, session_id):
        request_session = self.request.session
        user = self.user

        local_session = get_session_by_id(session_id=session_id)
        if not local_session:
            raise ValidationError(
                {"detail": ErrorDetail(_("Invalid session_id."))}
            )

        if request_session.session_key == local_session.session_key:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Can not delete current active session, Please use logout to end this session."
                        )
                    )
                }
            )

        if not self.check_session_exists(
            session_key=local_session.session_key
        ):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Invalid session key or session is already expired.")
                    )
                }
            )

        request_session.delete(local_session.session_key)
        local_session.expire_session()
        return True
