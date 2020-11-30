from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import NotAuthenticated

__all__ = ("AdminRoleRequiredMiddleware",)


class AdminRoleRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if path.startswith("/admin/") or path.startswith("/api/admin/"):
            if not (
                request.user.is_authenticated and request.user.is_admin_role()
            ):
                raise NotAuthenticated(detail="Invalid request.")
