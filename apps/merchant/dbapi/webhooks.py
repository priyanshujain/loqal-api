from apps.merchant.models import (BeneficialOwner,
                                  ControllerVerificationDocument,
                                  IncorporationVerificationDocument,
                                  OwnerVerificationDocument)


def get_incorporation_document(dwolla_id):
    try:
        return IncorporationVerificationDocument.objects.get(
            dwolla_id=dwolla_id
        )
    except IncorporationVerificationDocument.DoesNotExist:
        return None


def get_controller_document(dwolla_id):
    try:
        return ControllerVerificationDocument.objects.get(dwolla_id=dwolla_id)
    except ControllerVerificationDocument.DoesNotExist:
        return None


def get_owner_document(dwolla_id):
    try:
        return OwnerVerificationDocument.objects.get(dwolla_id=dwolla_id)
    except OwnerVerificationDocument.DoesNotExist:
        return None


def get_beneficial_owner_by_dwolla_id(dwolla_id):
    try:
        return BeneficialOwner.objects.get(dwolla_id=dwolla_id)
    except BeneficialOwner.DoesNotExist:
        return None
