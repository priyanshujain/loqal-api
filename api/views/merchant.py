from api.exceptions import NotAuthenticated, PermissionDenied
from apps.merchant.dbapi import get_account_member_by_user_id

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

        merchant_account_member = get_account_member_by_user_id(
            user_id=user.id
        )
        if not merchant_account_member:
            exception_message = "Merchant is not valid"
        else:
            request.merchant_account_member = merchant_account_member
            request.merchant_account = merchant_account_member.merchant
            request.account = request.merchant_account.account

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request
