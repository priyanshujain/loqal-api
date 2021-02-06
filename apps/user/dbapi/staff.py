from django.db.models import Q
from django.db.utils import IntegrityError

from apps.user.models import User
from apps.user.options import UserType

__all__ = (
    "create_staff_user",
    "get_admin_users",
)


def create_staff_user(
    email, password, first_name, last_name, user_type=UserType.ADMIN_STAFF
):
    try:
        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.gen_email_verification_token()
        user.verify_email()
        user.set_user_type(user_type=user_type)
    except IntegrityError:
        return None
    return user


def get_admin_users():
    return User.objects.filter(
        Q(user_type=UserType.REGULAR_STAFF) | Q(user_type=UserType.ADMIN_STAFF)
    )
