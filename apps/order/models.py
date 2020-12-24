from django.db import models
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField
from apps.account.models import ConsumerAccount, MerchantAccount
from .options import OrderStatus, OrderType
from django.conf import settings


class Order(AbstractBaseModel):
    consumer = models.ForeignKey(
        ConsumerAccount,
        related_name="orders",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    merchant = models.ForeignKey(
        MerchantAccount,
        related_name="orders",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    order_type = ChoiceCharEnumField(
        max_length=32, default=OrderType.IN_PERSON, enum_type=OrderType
    )
    status = ChoiceCharEnumField(
        max_length=32, default=OrderStatus.UNFULFILLED, enum_type=OrderStatus
    )
    total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    total_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    discount_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    discount_name = models.CharField(max_length=255, blank=True, null=True)
    customer_note = models.TextField(blank=True, default="")

    class Meta:
        db_table = "merchant_order"
