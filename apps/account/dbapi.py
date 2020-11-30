from django.db.utils import IntegrityError

from apps.account.models import Account


def get_account(account_id):
    try:
        return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return None


def create_customer_account(company_name, country):
    try:
        return Account.objects.create(
            company_name=company_name, country=country, is_customer=True,
        )
    except IntegrityError:
        return None
