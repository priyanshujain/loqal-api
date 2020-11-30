from django.db.utils import IntegrityError

from apps.user.models import User
from apps.user.options import UserType

__all__ = ("create_staff_user",)


def create_staff_user(email, password, first_name, last_name):
    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.verify_email()
        user.set_user_type(user_type=UserType.ADMIN_STAFF)
    except IntegrityError:
        return None
    return user
