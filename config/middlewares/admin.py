from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import NotAuthenticated

__all__ = ("AdminRoleRequiredMiddleware",)


class AdminRoleRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if path.startswith("/staff/") or path.startswith("/api/staff/"):
            if not (
                request.user.is_authenticated and request.user.is_staff()
            ):
                raise NotAuthenticated(detail="Invalid request.")
