import re
from django.db import IntegrityError

from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  IncorporationDetails)
from apps.merchant.options import VerificationDocumentStatus

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
    "update_beneficial_owner_status",
    "get_all_beneficial_owners",
    "update_beneficial_owner_document",
    "update_controller_document",
    "update_business_document",
)


def get_incorporation_details(merchant_id):
    try:
        return IncorporationDetails.objects.get(merchant_id=merchant_id)
    except IncorporationDetails.DoesNotExist:
        return None


def create_incorporation_details(merchant_id, **kwargs):
    try:
        return IncorporationDetails.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_incorporation_details(incorporation_details_id, **kwargs):
    return IncorporationDetails.objects.filter(
        id=incorporation_details_id
    ).update(**kwargs)


def get_incorporation_details(merchant_id):
    try:
        return IncorporationDetails.objects.get(merchant_id=merchant_id)
    except IncorporationDetails.DoesNotExist:
        return None


def create_incorporation_details(merchant_id, **kwargs):
    try:
        return IncorporationDetails.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_incorporation_details(incorporation_details_id, **kwargs):
    return IncorporationDetails.objects.filter(
        id=incorporation_details_id
    ).update(**kwargs)


def get_controller_details(merchant_id):
    try:
        return ControllerDetails.objects.get(merchant_id=merchant_id)
    except ControllerDetails.DoesNotExist:
        return None


def create_controller_details(merchant_id, **kwargs):
    try:
        return ControllerDetails.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_controller_details(merchant_id, **kwargs):
    return ControllerDetails.objects.filter(merchant_id=merchant_id).update(
        **kwargs
    )


def get_beneficial_owner(merchant_id, beneficial_owner_id):
    try:
        return BeneficialOwner.objects.get(
            merchant_id=merchant_id, id=beneficial_owner_id
        )
    except BeneficialOwner.DoesNotExist:
        return None


def get_all_beneficial_owners(merchant_id):
    return BeneficialOwner.objects.filter(
        merchant_id=merchant_id
    )


def create_beneficial_owner(merchant_id, **kwargs):
    try:
        return BeneficialOwner.objects.create(
            merchant_id=merchant_id,
            **kwargs,
        )
    except IntegrityError:
        return None


def update_beneficial_owner(merchant_id, beneficial_owner_id, **kwargs):
    return ControllerDetails.objects.filter(
        id=beneficial_owner_id, merchant_id=merchant_id
    ).update(**kwargs)


def delete_beneficial_owner(merchant_id, beneficial_owner_id):
    beneficial_owner = get_beneficial_owner(
        merchant_id=merchant_id, beneficial_owner_id=beneficial_owner_id
    )
    if beneficial_owner:
        return beneficial_owner.delete()
    else:
        return None


def update_beneficial_owner_status(beneficial_owner_id, dwolla_id, status):
    try:
        beneficial_owner = BeneficialOwner.objects.get(id=beneficial_owner_id)
    except BeneficialOwner.DoesNotExist:
        return
    beneficial_owner.add_dwolla_id(dwolla_id=dwolla_id, save=False)
    beneficial_owner.update_status(status=status)


def update_beneficial_owner_document(beneficial_owner_id, verification_document_id, verification_document_type):
        BeneficialOwner.objects.filter(id=beneficial_owner_id).update(
            verification_document_type=verification_document_type,
            verification_document_file_id=verification_document_id,
            verification_document_status=VerificationDocumentStatus.UPLOADED
        )


def update_controller_document(merchant_id, verification_document_id, verification_document_type):
        ControllerDetails.objects.filter(merchant_id=merchant_id).update(
            verification_document_type=verification_document_type,
            verification_document_file_id=verification_document_id,
            verification_document_status=VerificationDocumentStatus.UPLOADED
        )


def update_business_document(merchant_id, verification_document_id, verification_document_type):
        IncorporationDetails.objects.filter(merchant_id=merchant_id).update(
            verification_document_type=verification_document_type,
            verification_document_file_id=verification_document_id,
            verification_document_status=VerificationDocumentStatus.UPLOADED
        )
