from apps.payment.models import PaymentEvent
from apps.payment.options import PaymentEventType


def initiate_payment_event(payment_id):
    PaymentEvent.objects.create(
        payment_id, event_type=PaymentEventType.PAYMENT_INTIATED
    )


def capture_payment_event(payment_id, transaction_tracking_id):
    PaymentEvent.objects.create(
        payment_id,
        event_type=PaymentEventType.PAYMENT_CAPTURED,
        parameter={"transaction_tracking_id": transaction_tracking_id},
    )


def failed_payment_event(payment_id, transaction_tracking_id):
    PaymentEvent.objects.create(
        payment_id,
        event_type=PaymentEventType.PAYMENT_FAILED,
        parameter={"transaction_tracking_id": transaction_tracking_id},
    )


def partial_refund_payment_event(payment_id, refund_tracking_id):
    PaymentEvent.objects.create(
        payment_id,
        event_type=PaymentEventType.PAYMENT_PARTIALLY_REFUNDED,
        parameter={"refund_tracking_id": refund_tracking_id},
    )


def full_refund_payment_event(payment_id, refund_tracking_id):
    PaymentEvent.objects.create(
        payment_id,
        event_type=PaymentEventType.PAYMENT_FULLY_REFUNDED,
        parameter={"refund_tracking_id": refund_tracking_id},
    )


def dispute_payment_event(payment_id, dispute_tracking_id):
    PaymentEvent.objects.create(
        payment_id,
        event_type=PaymentEventType.PAYMENT_DISPUTED,
        parameter={"dispute_tracking_id": dispute_tracking_id},
    )
