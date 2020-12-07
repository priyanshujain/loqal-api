from api.exceptions import NotAuthenticated, PermissionDenied
from apps.account.dbapi import get_consumer_account

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
            exception_message = "User is not authenticated."
        
        if not user.contact_number_verified:
            exception_message = "User phone number is not verified."
            exception_class = PermissionDenied

        consumer_account = get_consumer_account(user_id=user.id)
        if not consumer_account:
            exception_message = "User is not valid"
        else:
            request.account = consumer_account.account
            request.consumer_account = consumer_account

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request
