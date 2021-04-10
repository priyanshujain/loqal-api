from django.db.utils import IntegrityError

from apps.invite.models import B2BInvite, B2CInvite


def create_b2c_invite(
    phone_number,
    merchant_id,
    phone_number_country="US",
    consumer_name="",
    email="",
):
    try:
        return B2CInvite.objects.create(
            phone_number=phone_number,
            merchant_id=merchant_id,
            phone_number_country=phone_number_country,
            consumer_name=consumer_name,
            email=email,
        )
    except IntegrityError:
        return None


def get_b2c_invites(
    merchant_id,
):
    return B2CInvite.objects.filter(
        merchant_id=merchant_id,
    )


def get_all_b2c_invites():
    return B2CInvite.objects.all()


def get_b2c_invite_by_phone_number(phone_number, phone_number_country):
    try:
        return B2CInvite.objects.get(
            phone_number=phone_number,
            phone_number_country=phone_number_country,
        )
    except B2CInvite.DoesNotExist:
        return None


def create_b2b_invite(
    merchant_id,
    phone_number="",
    phone_number_country="US",
    merchant_name="",
    email="",
):
    try:
        return B2BInvite.objects.create(
            phone_number=phone_number,
            merchant_id=merchant_id,
            phone_number_country=phone_number_country,
            merchant_name=merchant_name,
            email=email,
        )
    except IntegrityError:
        return None


def get_b2b_invites(
    merchant_id,
):
    return B2BInvite.objects.filter(
        merchant_id=merchant_id,
    )


def get_all_b2b_invites():
    return B2BInvite.objects.all()
