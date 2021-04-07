from django.db.utils import IntegrityError
from django.utils.crypto import constant_time_compare

from apps.invite.models import C2BInvite, C2CInvite
from apps.user.dbapi import consumer


def create_c2c_invite(
    phone_number,
    consumer_id,
    phone_number_country="US",
    consumer_name="",
    email="",
):
    try:
        return C2CInvite.objects.create(
            phone_number=phone_number,
            consumer_id=consumer_id,
            phone_number_country=phone_number_country,
            consumer_name=consumer_name,
            email=email,
        )
    except IntegrityError:
        return None


def get_c2c_invites(
    consumer_id,
):
    return C2CInvite.objects.filter(
        consumer_id=consumer_id,
    )


def get_all_c2c_invites():
    return C2CInvite.objects.all()


def get_c2c_invite_by_phone_number(phone_number, phone_number_country="US"):
    try:
        return C2CInvite.objects.get(
            phone_number=phone_number,
            phone_number_country=phone_number_country,
        )
    except C2CInvite.DoesNotExist:
        return None


def get_c2c_invite(phone_number, consumer_id, phone_number_country="US"):
    try:
        return C2CInvite.objects.get(
            phone_number=phone_number,
            consumer_id=consumer_id,
            phone_number_country=phone_number_country,
        )
    except C2CInvite.DoesNotExist:
        return None


def create_c2b_invite(
    consumer_id,
    phone_number="",
    phone_number_country="US",
    merchant_name="",
    email="",
):
    try:
        return C2BInvite.objects.create(
            phone_number=phone_number,
            consumer_id=consumer_id,
            phone_number_country=phone_number_country,
            merchant_name=merchant_name,
            email=email,
        )
    except IntegrityError:
        return None


def get_c2b_invites(
    consumer_id,
):
    return C2BInvite.objects.filter(
        consumer_id=consumer_id,
    )


def get_all_c2b_invites():
    return C2BInvite.objects.all()
