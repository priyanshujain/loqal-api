from django.db.models import Q
from django.db.utils import IntegrityError
from django.utils.timezone import now

from apps.metrics.models import (ConsumerSocialShareRecord,
                                 MerchanttoConsumerRating)


def create_merchant_to_consumer_rating(
    merchant_id,
    consumer_id,
    transaction_id,
):
    return MerchanttoConsumerRating.objects.create(
        merchant_id=merchant_id,
        consumer_id=consumer_id,
        transaction_id=transaction_id,
    )


def get_merchant_to_consumer_rating(
    consumer_id,
):
    return MerchanttoConsumerRating.objects.filter(
        consumer_id=consumer_id,
    )


def create_consumer_social_record(
    consumer_id,
    transaction_id,
    platform,
    content,
):
    return ConsumerSocialShareRecord.objects.create(
        consumer_id=consumer_id,
        transaction_id=transaction_id,
        platform=platform,
        content=content,
    )
