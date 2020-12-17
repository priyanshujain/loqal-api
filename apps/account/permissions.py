from rest_framework.permissions import BasePermission

from apps.account.options import AccountStatus


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

        if merchant_account.account_status != AccountStatus.PENDING:
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

        if merchant_account.account_status != AccountStatus.VERIFIED:
            return False

        return True
