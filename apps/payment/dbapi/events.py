from apps.payment.models import PaymentEvent
from apps.payment.options import PaymentEventType, TransactionTransferTypes
from utils.types import to_float


def initiate_payment_event(payment_id):
    PaymentEvent.objects.create(
        payment_id=payment_id, event_type=PaymentEventType.PAYMENT_INTIATED
    )


def capture_payment_event(
    payment_id,
    transaction_tracking_id,
    amount,
    transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
):
    PaymentEvent.objects.create(
        payment_id=payment_id,
        event_type=PaymentEventType.PAYMENT_CAPTURED,
        transfer_type=transfer_type,
        parameters={
            "transaction_tracking_id": transaction_tracking_id,
            "amount": to_float(amount),
        },
    )


def failed_payment_event(
    payment_id,
    transaction_tracking_id,
    amount,
    transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
):
    PaymentEvent.objects.create(
        payment_id=payment_id,
        event_type=PaymentEventType.PAYMENT_FAILED,
        transfer_type=transfer_type,
        parameters={
            "transaction_tracking_id": transaction_tracking_id,
            "amount": to_float(amount),
        },
    )


def failure_partial_return_event(
    payment_id,
    transaction_tracking_id,
    amount,
    transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
):
    PaymentEvent.objects.create(
        payment_id=payment_id,
        event_type=PaymentEventType.PARTIAL_FAILURE_RETURN,
        transfer_type=transfer_type,
        parameters={
            "transaction_tracking_id": transaction_tracking_id,
            "amount": to_float(amount),
        },
    )


def failed_refund_payment_event(
    payment_id,
    transaction_tracking_id,
    amount,
    transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
):
    PaymentEvent.objects.create(
        payment_id=payment_id,
        event_type=PaymentEventType.REFUND_FAILED,
        transfer_type=transfer_type,
        parameters={
            "transaction_tracking_id": transaction_tracking_id,
            "amount": to_float(amount),
        },
    )


def partial_refund_payment_event(
    payment_id,
    refund_tracking_id,
    transaction_tracking_id,
    amount,
    transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
):
    PaymentEvent.objects.create(
        payment_id=payment_id,
        event_type=PaymentEventType.PAYMENT_PARTIALLY_REFUNDED,
        transfer_type=transfer_type,
        parameters={
            "transaction_tracking_id": transaction_tracking_id,
            "refund_tracking_id": refund_tracking_id,
            "amount": to_float(amount),
        },
    )


def full_refund_payment_event(
    payment_id,
    refund_tracking_id,
    transaction_tracking_id,
    amount,
    transfer_type=TransactionTransferTypes.ACH_BANK_TRANSFER,
):
    PaymentEvent.objects.create(
        payment_id=payment_id,
        event_type=PaymentEventType.PAYMENT_FULLY_REFUNDED,
        transfer_type=transfer_type,
        parameters={
            "transaction_tracking_id": transaction_tracking_id,
            "refund_tracking_id": refund_tracking_id,
            "amount": to_float(amount),
        },
    )


def dispute_payment_event(payment_id, dispute_tracking_id):
    PaymentEvent.objects.create(
        payment_id=payment_id,
        event_type=PaymentEventType.PAYMENT_DISPUTED,
        parameters={"dispute_tracking_id": dispute_tracking_id},
    )
