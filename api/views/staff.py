from api.exceptions import APIException, NotAuthenticated, PermissionDenied

from .base import APIAccessLogView


class StaffAPIView(APIAccessLogView):
    """
    StaffAPIView
    """

    def initialize_request(self, request, *args, **kwargs):
        """
        TODO: Fill
        """
        exception_message = ""
        exception_class = APIException

        user = request.user
        if not user.is_authenticated:
            exception_message = "User not authenticated"
            exception_class = NotAuthenticated
        elif not user.is_admin_role():
            exception_message = "You do not have permission to this API"
            exception_class = PermissionDenied

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)
        return drf_request
