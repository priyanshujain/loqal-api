from apps.account.models import Account, ConsumerAccount, MerchantAccount


def get_account_by_dwolla_id(dwolla_id):
    try:
        return Account.objects.get(dwolla_id=dwolla_id)
    except Account.DoesNotExist:
        return None
