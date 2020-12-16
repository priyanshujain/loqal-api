from django.db.utils import IntegrityError

from apps.account.models import Account, ConsumerAccount

__all__ = (
    "get_account",
    "create_consumer_account",
    "get_consumer_account",
    "check_account_username",
)


def get_account(account_id):
    try:
        return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return None


def create_consumer_account(user_id, username):
    account = Account.objects.create()
    try:
        return ConsumerAccount.objects.create(account=account, user_id=user_id, username=username)
    except IntegrityError:
        account.delete()
        return None


def get_consumer_account(user_id):
    try:
        return ConsumerAccount.objects.get(user_id=user_id)
    except ConsumerAccount.DoesNotExist:
        return None


def check_account_username(username):
    try:
        return ConsumerAccount.objects.filter(username=username).exists()
    except ConsumerAccount.DoesNotExist:
        return False
