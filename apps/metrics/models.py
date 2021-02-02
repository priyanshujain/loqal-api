from django.db import models

from apps.account.models import ConsumerAccount, MerchantAccount
from apps.payment.models import Transaction
from db.models import AbstractBaseModel


class MerchanttoConsumerRating(AbstractBaseModel):
    merchant = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE)
    consumer = models.ForeignKey(ConsumerAccount, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    give_thanks = models.BooleanField(default=True)

    class Meta:
        db_table = "merchant_to_consumer_rating"


class ConsumerSocialShareRecord(AbstractBaseModel):
    consumer = models.ForeignKey(ConsumerAccount, on_delete=models.CASCADE)
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, null=True, blank=True
    )
    platform = models.CharField(blank=True, max_length=64)
    content = models.CharField(blank=True, max_length=256)

    class Meta:
        db_table = "consumer_social_share"
