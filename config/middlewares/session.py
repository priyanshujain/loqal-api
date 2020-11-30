from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from ipware import get_client_ip

__all__ = ("SessionRecordMiddleware",)


class SessionRecordMiddleware(MiddlewareMixin):
    # TODO: Combine cache based session and models based session so that
    #       we have a record of expired sessions.
    # TODO: Check if IP changes in the middle of a session
    def process_request(self, request):
        request.ip, is_routable = get_client_ip(request)
        session = request.session
        meta = request.META
        session["ip"] = request.ip
        session["is_ip_routable"] = is_routable
        session["last_activity"] = now()
        session["user_agent"] = meta.get("HTTP_USER_AGENT", "")
        # Cloudflare request tags
        session["cf_request_id"] = meta.get("HTTP_CF_REQUEST_ID", "")
        session["cf_connecting_ip"] = meta.get("HTTP_CF_CONNECTING_IP", "")
        session["cf_ip_country"] = meta.get("HTTP_CF_IPCOUNTRY", "")
        session["cf_ray_id"] = meta.get("HTTP_CF_RAY", "")
