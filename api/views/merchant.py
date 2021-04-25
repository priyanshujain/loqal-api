from api.exceptions import NotAuthenticated, PermissionDenied
from apps.merchant.dbapi import (get_account_member_by_user_id,
                                 get_active_pos_session)

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

        if user.is_authenticated and user.is_disabled:
            exception_message = "Your account has been de-activated. Please contact our support team."
            exception_class = PermissionDenied

        merchant_account_member = get_account_member_by_user_id(
            user_id=user.id
        )
        if not merchant_account_member:
            exception_message = "Merchant is not valid"
        else:
            request.merchant_account_member = merchant_account_member
            request.merchant_account = merchant_account_member.merchant
            request.account = request.merchant_account.account

            if not request.account.is_active:
                exception_message = "Your account has been de-activated. Please contact our support team."
                exception_class = PermissionDenied

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request


class PosStaffAPIView(APIAccessLogView):
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

        if user.is_authenticated and user.is_disabled:
            exception_message = "Your account has been de-activated. Please contact our support team."
            exception_class = PermissionDenied

        pos_session = get_active_pos_session(
            user_id=user.id, user_session_key=request.session.session_key
        )
        if not pos_session:
            exception_message = "POS session is not valid"
        else:
            request.pos_session = pos_session
            request.pos_staff = pos_session.staff
            request.merchant_account = pos_session.staff.merchant
            request.account = request.merchant_account.account

            if not request.account.is_active:
                exception_message = "Your account has been de-activated. Please contact our support team."
                exception_class = PermissionDenied

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request
