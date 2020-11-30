from api.exceptions import APIException, NotAuthenticated, PermissionDenied

from .base import APIAccessLogView


class UserAPIView(APIAccessLogView):
    """
    UserAPIView
    """

    def initialize_request(self, request, *args, **kwargs):
        """
        # TODO: Fill
        """
        exception_message = ""
        exception_class = NotAuthenticated
        user = request.user

        if not user.is_authenticated:
            exception_message = "User not authenticated"
            exception_class = NotAuthenticated

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request
