from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ProviderAPIException, ValidationError
from api.services import ServiceBase
from apps.account.options import AccountCerficationStatus, DwollaCustomerStatus
from apps.provider.lib.actions import ProviderAPIActionBase

__all__ = ("CertifyDwollaMerchantAccount",)


class CertifyDwollaMerchantAccount(ServiceBase):
    is_all_verified = True

    def __init__(self, merchant):
        self.merchant = merchant

    def handle(self):
        merchant = self.merchant
        if (
            merchant.account.dwolla_customer_status
            == DwollaCustomerStatus.VERIFIED
            and merchant.account.is_certification_required
            and merchant.account.certification_status
            != AccountCerficationStatus.CERTIFIED
        ):
            self._certify_beneficial_owners(merchant=merchant)
        else:
            raise ValidationError(
                {"detail": ErrorDetail(_("Certification is not required."))}
            )
        return merchant

    def _certify_beneficial_owners(self, merchant):
        certification = DwollaCertifyBeneficialOwnerAPIAction(
            account_id=merchant.account.id
        ).certify()
        merchant.account.update_certification_status(
            status=certification["status"]
        )


class DwollaCertifyBeneficialOwnerAPIAction(ProviderAPIActionBase):
    def certify(self):
        response = self.client.account.certify_beneficial_owner()
        if self.get_errors(response):
            raise ProviderAPIException(
                {
                    "detail": ErrorDetail(
                        _(
                            "KYC service failed, Please try "
                            "again. If the problem persists please "
                            "contact our support team."
                        )
                    )
                }
            )
        return {
            "status": response["data"].get("status"),
        }
