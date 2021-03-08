from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from apps.account.models import Account, ConsumerAccount, MerchantAccount
from db.models import AbstractBaseModel, BaseModel
from db.models.fields import ChoiceCharEnumField
from db.models.fields.enum import ChoiceEnumField

from .options import DiscountType, OrderEventType, OrderStatus, OrderType


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
    total_return_amount = models.DecimalField(
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
    discount_type = ChoiceCharEnumField(
        max_length=32,
        default=DiscountType.FIXED_AMOUNT,
        enum_type=DiscountType,
    )
    is_paid = models.BooleanField(default=False)
    is_rewarded = models.BooleanField(default=False)

    # Reward given for the order
    cash_reward = models.ForeignKey(
        to="reward.CashReward",
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )
    voucher_reward = models.ForeignKey(
        to="reward.VoucherReward",
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )
    customer_note = models.TextField(blank=True, default="")
    order_tracking_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
        unique=True,
        editable=False,
    )

    class Meta:
        db_table = "merchant_order"

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.order_tracking_id:
            self.order_tracking_id = id_generator()
            while Order.objects.filter(
                order_tracking_id=self.order_tracking_id
            ).exists():
                self.order_tracking_id = id_generator()
        return super().save(*args, **kwargs)

    def mark_paid(self, save=False):
        self.is_paid = True
        if save:
            self.save()

    def set_fulfilled(self, save=True):
        self.status = OrderStatus.FULFILLED
        if save:
            self.save()

    def set_partially_fulfilled(self, save=True):
        self.status = OrderStatus.PARTIALLY_FULFILLED
        if save:
            self.save()

    def set_partially_returned(self, amount, save=True):
        self.status = OrderStatus.PARTIALLY_RETURNED
        self.total_return_amount += amount
        if save:
            self.save()

    def set_returned(self, amount, save=True):
        self.status = OrderStatus.RETURNED
        self.total_return_amount += amount
        if save:
            self.save()

    def set_cancelled(self, save=True):
        self.status = OrderStatus.CANCELLED
        if save:
            self.save()

    def update_discount(self, amount, name="", save=True):
        self.discount_amount += amount
        self.total_net_amount -= amount
        self.discount_name = name
        if save:
            self.save()


class OrderEvent(BaseModel):
    """
    Model used to store events that happened during the order lifecycle.

    """

    event_type = ChoiceEnumField(enum_type=OrderEventType)
    order = models.ForeignKey(
        Order, related_name="events", on_delete=models.CASCADE
    )
    parameters = models.JSONField(blank=True, default=dict)
    account = models.ForeignKey(
        Account,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="order_events",
    )

    class Meta:
        db_table = "order_event"
