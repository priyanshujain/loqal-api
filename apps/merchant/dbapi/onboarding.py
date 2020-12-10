from django.db import IntegrityError

from apps.merchant.models import (
    IncorporationDetails,
    ControllerDetails,
    BeneficialOwner,
)

__all__ = (
    "get_incorporation_details",
    "create_incorporation_details",
    "update_incorporation_details",
    "get_controller_details",
    "create_controller_details",
    "update_controller_details",
    "get_beneficial_owner",
    "create_beneficial_owner",
    "update_beneficial_owner",
    "delete_beneficial_owner",
)


def get_incorporation_details(merchant_id):
    try:
        return IncorporationDetails.objects.get(merchant_id=merchant_id)
    except IncorporationDetails.DoesNotExist:
        return None


def create_incorporation_details(
    merchant_id,
    **kwargs
):
    try:
        return IncorporationDetails.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_incorporation_details(incorporation_details_id, **kwargs):
    return IncorporationDetails.objects.filter(id=incorporation_details_id).update(
        **kwargs
    )


def get_incorporation_details(merchant_id):
    try:
        return IncorporationDetails.objects.get(merchant_id=merchant_id)
    except IncorporationDetails.DoesNotExist:
        return None


def create_incorporation_details(
    merchant_id,
    **kwargs
):
    try:
        return IncorporationDetails.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_incorporation_details(incorporation_details_id, **kwargs):
    return IncorporationDetails.objects.filter(id=incorporation_details_id).update(
        **kwargs
    )


def get_controller_details(merchant_id):
    try:
        return ControllerDetails.objects.get(merchant_id=merchant_id)
    except ControllerDetails.DoesNotExist:
        return None


def create_controller_details(
    merchant_id,
    **kwargs
):
    try:
        return ControllerDetails.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_controller_details(merchant_id, controller_id, **kwargs):
    return ControllerDetails.objects.filter(id=controller_id, merchant_id=merchant_id).update(
        **kwargs
    )


def get_beneficial_owner(merchant_id, beneficial_owner_id):
    try:
        return BeneficialOwner.objects.get(merchant_id=merchant_id, id=beneficial_owner_id)
    except BeneficialOwner.DoesNotExist:
        return None


def create_beneficial_owner(
    merchant_id,
    **kwargs
):
    try:
        return BeneficialOwner.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_beneficial_owner(merchant_id, beneficial_owner_id, **kwargs):
    return ControllerDetails.objects.filter(id=beneficial_owner_id, merchant_id=merchant_id).update(
        **kwargs
    )


def delete_beneficial_owner(merchant_id, beneficial_owner_id):
    beneficial_owner = get_beneficial_owner(merchant_id=merchant_id, id=beneficial_owner_id)
    if beneficial_owner:
        return beneficial_owner.delete()
    else:
        return None