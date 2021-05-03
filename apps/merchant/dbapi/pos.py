from django.db.models import Q
from django.db.utils import IntegrityError
from django.utils.timezone import now

from apps.merchant.models import PosSession, PosStaff
from apps.user.dbapi import create_user
from apps.user.models import User
from apps.user.options import CustomerTypes


def get_merchant_user(email, phone_number):
    users = User.objects.filter(customer_type=CustomerTypes.MERCHANT).filter(
        Q(email=email) | Q(phone_number=phone_number)
    )
    if users.exists():
        return users.first()
    return None


def check_staff_exists(user_id, merchant_id):
    return PosStaff.objects.filter(
        merchant_id=merchant_id, user_id=user_id
    ).exists()


def get_staff_from_username(username):
    staff = PosStaff.objects.filter(user__username=username)
    if staff.exists():
        return staff.first()
    return None


def get_pos_staff(pos_staff_id, merchant_id):
    try:
        return PosStaff.objects.get(
            merchant_id=merchant_id,
            u_id=pos_staff_id,
        )
    except PosStaff.DoesNotExist:
        return None


def check_existing_pos_staff(email, phone_number, merchant_id):
    staff = PosStaff.objects.filter(
        merchant_id=merchant_id,
        user__customer_type=CustomerTypes.MERCHANT,
        user__email=email,
        user__phone_number=phone_number,
    )
    if staff.exists():
        return staff.first()
    return None


def get_merchant_pos_staff(merchant_id):
    return PosStaff.objects.filter(
        merchant_id=merchant_id,
    )


def create_pos_staff(
    merchant_id,
    first_name,
    last_name,
    email,
    phone_number,
    register_id,
    shift_start=None,
    shift_end=None,
):
    try:
        user = create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=email,
            customer_type=CustomerTypes.MERCHANT,
            email_verified=False,
        )
    except IntegrityError:
        return None

    try:
        pos_staff = PosStaff.objects.create(
            user=user,
            merchant_id=merchant_id,
            account_active=True,
            shift_start=shift_start,
            shift_end=shift_end,
            register_id=register_id,
        )
        pos_staff.generate_login_token()
        return pos_staff
    except IntegrityError:
        user.delete()
        return None


def update_pos_staff(
    pos_staff,
    first_name,
    last_name,
    email,
    phone_number,
    register_id,
    shift_start=None,
    shift_end=None,
):
    user = pos_staff.user
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone_number = phone_number
    user.username = f"{email}::{CustomerTypes.MERCHANT}"
    user.save()

    pos_staff.register_id = register_id
    pos_staff.shift_start = shift_start
    pos_staff.shift_end = shift_end
    pos_staff.save()


def create_pos_session(staff_id, user_session_id, expires_at):
    try:
        return PosSession.objects.create(
            staff_id=staff_id,
            expires_at=expires_at,
            login_session_id=user_session_id,
        )
    except IntegrityError:
        return None


def get_active_pos_session(user_id, user_session_key):
    sessions = PosSession.objects.filter(
        staff__user_id=user_id,
        login_session__session_key=user_session_key,
        expires_at__gt=now(),
    )
    if sessions.exists():
        return sessions.first()
    return None


def expire_all_active_pos_session(user_id):
    sessions = PosSession.objects.filter(
        staff__user_id=user_id,
        expires_at__gt=now(),
    ).update(expires_at=now())


def all_active_pos_sessions(merchant_id):
    return PosSession.objects.filter(
        staff__merchant_id=merchant_id,
        expires_at__gt=now(),
    )
