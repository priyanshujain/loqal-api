from django.db.utils import IntegrityError

from apps.account.models import Account, ConsumerAccount

__all__ = (
    "get_account",
    "create_consumer_account",
    "get_consumer_account",
)


def get_account(account_id):
    try:
        return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return None


def create_consumer_account(user_id):
    account = Account.objects.create()
    try:
        return ConsumerAccount.objects.create(account=account, user_id=user_id)
    except IntegrityError:
        account.delete()
        return None


def get_consumer_account(user_id):
    try:
        return ConsumerAccount.objects.get(user_id=user_id)
    except ConsumerAccount.DoesNotExist:
        return None
