import re

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from api.exceptions import NotAuthenticated, PermissionDenied
from apps.account.dbapi import get_consumer_account

from .base import APIAccessLogView


class ConsumerAPIView(APIAccessLogView):
    """
    ConsumerAPIView
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerAPIView, self).dispatch(request, *args, **kwargs)

    def initialize_request(self, request, *args, **kwargs):
        """
        # TODO: Fill
        """
        exception_message = ""
        exception_class = NotAuthenticated
        user = request.user

        if not user.is_authenticated:
            exception_message = "User is not authenticated."

        if user.is_authenticated and not user.phone_number_verified:
            exception_message = "User phone number is not verified."
            exception_class = PermissionDenied

        consumer_account = get_consumer_account(user_id=user.id)
        if not consumer_account:
            exception_message = "Account is not valid"
        else:
            if not consumer_account.account:
                exception_message = "Account is not valid"
            request.account = consumer_account.account

            if not request.account.is_active:
                exception_message = "Your account has been de-activated. Please contact our support team."
                exception_class = PermissionDenied
            request.consumer_account = consumer_account

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request


class ConsumerPre2FaAPIView(APIAccessLogView):
    """
    ConsumerAPIView
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConsumerPre2FaAPIView, self).dispatch(request, *args, **kwargs)

    def initialize_request(self, request, *args, **kwargs):
        """
        # TODO: Fill
        """
        exception_message = ""
        exception_class = NotAuthenticated
        user = request.user

        if not user.is_authenticated:
            exception_message = "User is not authenticated."

        consumer_account = get_consumer_account(user_id=user.id)
        if not consumer_account:
            exception_message = "User is not valid"
        else:
            request.account = consumer_account.account
            if not request.account.is_active:
                exception_message = "Your account has been de-activated. Please contact our support team."
                exception_class = PermissionDenied
            request.consumer_account = consumer_account

        drf_request = super().initialize_request(request, *args, **kwargs)
        if exception_message:
            raise exception_class(detail=exception_message)

        return drf_request
