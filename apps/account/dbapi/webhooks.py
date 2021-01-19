from apps.account.models import MerchantAccount, ConsumerAccount, Account


def get_account(dwolla_id):
    try:
        return Account.objects.get(dwolla_id=dwolla_id)
    except Account.DoesNotExist:
        return None

