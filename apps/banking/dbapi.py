"""
DB operations related to bank accounts
"""
from django.db import IntegrityError

from apps.banking.models import BankAccount

__all__ = (
    "create_bank_account",
    "get_bank_account",
    "update_bank_account",
    "get_bank_account_by_dwolla_id",
)


def create_bank_account(
    account_id,
    plaid_access_token,
    plaid_account_id,
    account_number_suffix,
    bank_name,
    bank_logo_base64,
    name,
):
    """
    dbapi to create a bank account instance.
    """
    try:
        return BankAccount.objects.create(
            account_id=account_id,
            plaid_access_token=plaid_access_token,
            plaid_account_id=plaid_account_id,
            account_number_suffix=account_number_suffix,
            bank_name=bank_name,
            bank_logo_base64=bank_logo_base64,
            name=name,
        )
    except IntegrityError:
        return None


def get_bank_account(account_id):
    """
    dbapi to get bank account for a given account
    """
    try:
        return BankAccount.objects.get(
            account_id=account_id,
            is_primary=True,
        )
    except BankAccount.DoesNotExist:
        return None


def update_bank_account(bank_account_id, plaid_access_token, plaid_account_id):
    """
    dbapi to updates a bank account instance.
    """
    BankAccount.objects.filter(id=bank_account_id).update(
        plaid_access_token=plaid_access_token,
        plaid_account_id=plaid_account_id,
    )


def get_bank_account_by_dwolla_id(dwolla_id):
    """
    dbapi to get bank account for a given dwolla_id
    """
    try:
        return BankAccount.objects.get(
            dwolla_id=dwolla_id,
        )
    except BankAccount.DoesNotExist:
        return None
