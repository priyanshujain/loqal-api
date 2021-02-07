from apps.account.models import MerchantAccount
from apps.merchant.models import (CodesAndProtocols, MerchantCategory,
                                  MerchantOperationHours, MerchantProfile,
                                  ServiceAvailability)


def delete_non_loqal(merchant_id):
    MerchantCategory.objects.filter(merchant_id=merchant_id).delete()
    MerchantProfile.objects.filter(merchant_id=merchant_id).delete()
    MerchantOperationHours.objects.filter(merchant_id=merchant_id).delete()
    CodesAndProtocols.objects.filter(merchant_id=merchant_id).delete()
    ServiceAvailability.objects.filter(merchant_id=merchant_id).delete()
    MerchantAccount.objects.filter(id=merchant_id).delete()
