from rest_framework.permissions import BasePermission

from apps.member.options import FeatureAcessTypes


class CreatePaymentPermission(BasePermission):
    """
    Check if user has permission to create payment
    """

    message = "You are not allowed to create new payment, please contact account admin."

    def has_permission(self, request, view):
        account_member = request.account_member
        if FeatureAcessTypes.CREATE not in account_member.role.transactions:
            return False
        return True
