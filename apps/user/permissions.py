from rest_framework.permissions import BasePermission


class IsAdminStaffPermission(BasePermission):
    """
    Check if user is admin staff member.
    """

    message = "Contact CO/XO."

    def has_permission(self, request, view):
        user = request.user
        if user.is_admin_staff():
            return True
        return False


class IsStaffPermission(BasePermission):
    """
    Check if user is staff member.
    """

    message = "Contact CO/XO."

    def has_permission(self, request, view):
        user = request.user
        if user.is_staff():
            return True
        return False
