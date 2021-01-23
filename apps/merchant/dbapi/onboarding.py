import re

from django.db import IntegrityError

from apps.merchant.models import (BeneficialOwner, ControllerDetails,
                                  ControllerVerificationDocument,
                                  IncorporationDetails,
                                  IncorporationVerificationDocument,
                                  OwnerVerificationDocument)
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
    "create_beneficial_owner_document",
    "create_controller_document",
    "create_business_document",
    "update_beneficial_owner_document",
    "update_controller_document",
    "update_business_document",
    "get_beneficial_owner_document",
    "get_controller_document",
    "get_business_document",
    "get_merchant_beneficial_owner_document",
    "get_merchant_controller_document",
    "get_merchant_business_document",
    "get_incorporation_details_by_ein",
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


def get_incorporation_details_by_ein(ein_number):
    try:
        return IncorporationDetails.objects.get(ein_number=ein_number)
    except IncorporationDetails.DoesNotExist:
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
    return BeneficialOwner.objects.filter(merchant_id=merchant_id)


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


def create_beneficial_owner_document(
    owner_id, document_file_id, document_type
):
    try:
        return OwnerVerificationDocument.objects.create(
            owner_id=owner_id,
            document_type=document_type,
            document_file_id=document_file_id,
            status=VerificationDocumentStatus.UPLOADED,
        )
    except IntegrityError:
        return None


def create_controller_document(controller_id, document_file_id, document_type):
    try:
        return ControllerVerificationDocument.objects.create(
            controller_id=controller_id,
            document_type=document_type,
            document_file_id=document_file_id,
            status=VerificationDocumentStatus.UPLOADED,
        )
    except IntegrityError:
        return None


def create_business_document(
    incorporation_details_id, document_file_id, document_type
):
    try:
        return IncorporationVerificationDocument.objects.create(
            incorporation_details_id=incorporation_details_id,
            document_type=document_type,
            document_file_id=document_file_id,
            status=VerificationDocumentStatus.UPLOADED,
        )
    except IntegrityError:
        return None


def update_beneficial_owner_document(
    document, document_file_id, document_type
):
    document.document_type = document_type
    document.document_file_id = document_file_id
    document.status = VerificationDocumentStatus.UPLOADED
    document.save()
    return document


def update_controller_document(document, document_file_id, document_type):
    document.document_type = document_type
    document.document_file_id = document_file_id
    document.status = VerificationDocumentStatus.UPLOADED
    document.save()
    return document


def update_business_document(document, document_file_id, document_type):
    document.document_type = document_type
    document.document_file_id = document_file_id
    document.status = VerificationDocumentStatus.UPLOADED
    document.save()
    return document


def get_beneficial_owner_document(document_id, owner_id):
    try:
        return OwnerVerificationDocument.objects.get(
            u_id=document_id, owner_id=owner_id
        )
    except OwnerVerificationDocument.DoesNotExist:
        return None


def get_controller_document(document_id, controller_id):
    try:
        return ControllerVerificationDocument.objects.get(
            u_id=document_id, controller_id=controller_id
        )
    except ControllerVerificationDocument.DoesNotExist:
        return None


def get_business_document(document_id, incorporation_details_id):
    try:
        return IncorporationVerificationDocument.objects.get(
            u_id=document_id, incorporation_details_id=incorporation_details_id
        )
    except IncorporationVerificationDocument.DoesNotExist:
        return None


def get_merchant_beneficial_owner_document(owner_id):
    return OwnerVerificationDocument.objects.filter(owner_id=owner_id)


def get_merchant_controller_document(controller_id):
    return ControllerVerificationDocument.objects.filter(
        controller_id=controller_id
    )


def get_merchant_business_document(incorporation_details_id):
    return IncorporationVerificationDocument.objects.filter(
        incorporation_details_id=incorporation_details_id
    )
