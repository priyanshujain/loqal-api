from api.exceptions import NotAuthenticated, PermissionDenied
from apps.account.dbapi import get_merchant_account

from .base import APIAccessLogView


class MerchantAPIView(APIAccessLogView):
    """
    ConsumerAPIView
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


        merchant_account = get_merchant_account(user_id=user.id)
        if not merchant_account:
            exception_message = "User is not valid"
        else:
            request.account = merchant_account.account
            request.merchant_account = merchant_account

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request
