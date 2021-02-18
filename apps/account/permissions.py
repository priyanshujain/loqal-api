from rest_framework.permissions import BasePermission

from apps.account.options import DwollaCustomerStatus


class IsMerchantAccountPendingPermission(BasePermission):
    """
    Check if account has been approved by the provider
    """

    message = "The account has been already approved."

    def has_permission(self, request, view):
        try:
            merchant_account = request.merchant_account
        except AttributeError:
            return False

        if (
            merchant_account.account.dwolla_customer_status
            == DwollaCustomerStatus.VERIFIED
        ):
            return False

        return True


class IsMerchantAccountVerifiedPermission(BasePermission):
    """
    Check if account has been approved by the provider
    """

    message = "The account has been already approved."

    def has_permission(self, request, view):
        try:
            merchant_account = request.merchant_account
        except AttributeError:
            return False

        if (
            merchant_account.account.dwolla_customer_status
            != DwollaCustomerStatus.VERIFIED
        ):
            return False

        return True


class IsMerchantAccountEnabledPermission(BasePermission):
    """
    Check if account has been approved by the provider
    """

    message = "The account has been already approved."

    def has_permission(self, request, view):
        try:
            merchant_account = request.merchant_account
        except AttributeError:
            return False

        if merchant_account.account.is_active:
            return True

        return False
