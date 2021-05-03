from celery import shared_task

from apps.account.options import AccountCerficationStatus, DwollaCustomerStatus
from apps.banking.dbapi import get_bank_account
from apps.merchant.dbapi import pos
from apps.merchant.models import StoreImage
from utils.thumbnails import create_thumbnails


def check_if_merchant_account_ready(merchant):
    account = merchant.account
    if not account:
        return False
    if account.dwolla_customer_status != DwollaCustomerStatus.VERIFIED:
        return False
    if (
        account.is_certification_required
        and account.certification_status != AccountCerficationStatus.CERTIFIED
    ):
        return False
    bank_account = get_bank_account(account_id=account.id)
    if not bank_account:
        return False
    if not bank_account.is_payment_allowed():
        return False
    return True


@shared_task
def create_store_image_thumbnails(image_id):
    """Create thumbnails for store images."""
    create_thumbnails(
        pk=image_id, model=StoreImage, size_set="stores", image_attr="image"
    )
