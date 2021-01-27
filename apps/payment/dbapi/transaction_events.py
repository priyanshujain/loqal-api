from django.db.utils import IntegrityError

from apps.payment.models import TransactionEvent

__all__ = ("create_transaction_event",)


def create_transaction_event(
    transaction_id, event_type, event_timestamp, parameters={}
):
    try:
        return TransactionEvent.objects.create(
            transaction_id=transaction_id,
            event_type=event_type,
            event_timestamp=event_timestamp,
            parameters=parameters,
        )
    except IntegrityError:
        return None
