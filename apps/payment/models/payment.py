from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from apps.order.models import Order
from apps.payment.options import (ChargeStatus, PaymentEventType,
                                  PaymentMethodType, PaymentProcess,
                                  PaymentStatus)
from apps.provider.options import DEFAULT_CURRENCY
from db.models import AbstractBaseModel
from db.models.fields import ChoiceCharEnumField, ChoiceEnumField

__all__ = (
    "Payment",
    "PaymentEvent",
)


class Payment(AbstractBaseModel):
    """
    This represents payment status for a single order
    """

    gateway = models.CharField(max_length=64, default="dwolla")
    payment_method_type = ChoiceCharEnumField(
        max_length=64,
        default=PaymentMethodType.ACH,
        enum_type=PaymentMethodType,
    )
    payment_process = ChoiceEnumField(
        enum_type=PaymentProcess, default=PaymentProcess.NOT_PROVIDED
    )
    captured_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    total_tip_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    refunded_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    payment_currency = models.CharField(max_length=3, default=DEFAULT_CURRENCY)
    charge_status = ChoiceEnumField(
        enum_type=ChargeStatus, default=ChargeStatus.NOT_CHARGED
    )
    order = models.OneToOneField(
        Order, related_name="payment", on_delete=models.CASCADE
    )
    payment_tracking_id = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=None,
        unique=True,
        editable=False,
    )
    status = ChoiceEnumField(
        enum_type=PaymentStatus,
    )

    class Meta:
        db_table = "payment"

    def save(self, *args, **kwargs):
        def id_generator():
            return get_random_string(
                length=10, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )

        if not self.payment_tracking_id:
            self.payment_tracking_id = id_generator()
            while Payment.objects.filter(
                payment_tracking_id=self.payment_tracking_id
            ).exists():
                self.payment_tracking_id = id_generator()
        return super().save(*args, **kwargs)

    def update_charge_status_by_refund(self, amount, save=True):
        self.refunded_amount += amount
        if self.refunded_amount < self.order.total_net_amount:
            self.charge_status = ChargeStatus.PARTIALLY_REFUNDED
            self.order.set_partially_returned(amount)
        elif self.refunded_amount == self.order.total_net_amount:
            self.charge_status = ChargeStatus.FULLY_REFUNDED
            self.order.set_returned(amount)
        if save:
            self.save()

    def capture_payment(self, amount, amount_towards_order, save=True):
        self.status = PaymentStatus.CAPTURED
        self.captured_amount += amount
        self.total_tip_amount += amount - amount_towards_order
        if amount_towards_order < self.order.total_net_amount:
            self.charge_status = ChargeStatus.PARTIALLY_CHARGED
            self.order.set_partially_fulfilled()
        elif amount_towards_order == self.order.total_net_amount:
            self.charge_status = ChargeStatus.FULLY_CHARGED
            self.order.mark_paid()
            self.order.set_fulfilled()
        else:
            self.charge_status = ChargeStatus.OTHER

        if save:
            self.save()

    def failed_payment(self, save=True):
        if self.status == PaymentStatus.IN_PROGRESS:
            self.status = PaymentStatus.FAILED
            if save:
                self.save()

    def cancelled_payment(self, save=True):
        if self.status == PaymentStatus.IN_PROGRESS:
            self.status = PaymentStatus.CANCELLED
            self.order.set_cancelled()
            if save:
                self.save()
    
    def process_zero_payment(self, save=True):
        self.status = PaymentStatus.CAPTURED
        self.charge_status = ChargeStatus.FULLY_CHARGED
        self.order.mark_paid()
        self.order.set_fulfilled()
        if save:
            self.save()

        


class PaymentEvent(AbstractBaseModel):
    payment = models.ForeignKey(
        Payment,
        blank=True,
        null=True,
        related_name="events",
        on_delete=models.CASCADE,
    )
    event_type = ChoiceEnumField(enum_type=PaymentEventType)
    parameters = models.JSONField(blank=True, default=dict)

    class Meta:
        db_table = "payment_event"
