from django.db.utils import IntegrityError

from apps.banking.options import VerificationProvider
from apps.core.models import AppMetaData, MerchantMetaData


def create_app_metadata(
    min_allowed_version,
    new_version,
    platform,
    store_url,
    api_env,
    primary_banking_verification_provider=VerificationProvider.PLAID,
):
    try:
        return AppMetaData.objects.create(
            min_allowed_version=min_allowed_version,
            new_version=new_version,
            platform=platform,
            store_url=store_url,
            api_env=api_env,
            primary_banking_verification_provider=primary_banking_verification_provider,
        )
    except IntegrityError:
        return None


def update_app_metadata(
    min_allowed_version,
    new_version,
    platform,
    store_url,
    api_env,
    primary_banking_verification_provider=VerificationProvider.PLAID,
):
    qs = AppMetaData.objects.filter(platform=platform).update(
        min_allowed_version=min_allowed_version,
        new_version=new_version,
        store_url=store_url,
        api_env=api_env,
        primary_banking_verification_provider=primary_banking_verification_provider,
    )


def get_app_metadata():
    return AppMetaData.objects.all()


def get_platform_app_metadata(platform):
    try:
        return AppMetaData.objects.get(platform=platform)
    except AppMetaData.DoesNotExist:
        return None


def create_merchant_metadata(
    min_allowed_version,
    new_version,
    platform,
    store_url,
    api_env,
    primary_banking_verification_provider=VerificationProvider.PLAID,
):
    try:
        return MerchantMetaData.objects.create(
            min_allowed_version=min_allowed_version,
            new_version=new_version,
            platform=platform,
            store_url=store_url,
            api_env=api_env,
            primary_banking_verification_provider=primary_banking_verification_provider,
        )
    except IntegrityError:
        return None


def update_merchant_metadata(
    min_allowed_version,
    new_version,
    platform,
    store_url,
    api_env,
    primary_banking_verification_provider=VerificationProvider.PLAID,
):
    qs = MerchantMetaData.objects.filter(platform=platform).update(
        min_allowed_version=min_allowed_version,
        new_version=new_version,
        store_url=store_url,
        api_env=api_env,
        primary_banking_verification_provider=primary_banking_verification_provider,
    )


def get_merchant_metadata():
    return MerchantMetaData.objects.all()


def get_platform_merchant_metadata(platform):
    try:
        return MerchantMetaData.objects.get(platform=platform)
    except MerchantMetaData.DoesNotExist:
        return None
