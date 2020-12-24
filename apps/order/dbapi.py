from apps.order.models import Order
from apps.order.options import OrderType
from django.db.utils import IntegrityError


def create_payment_request_order(merchant_id, consumer_id, amount):
    """
    Create an order for payment request 
    """
    try:
        return Order.objects.create(
            merchant_id=merchant_id,
            consumer_id=consumer_id,
            total_net_amount=amount,
            total_amount=amount,
            order_type=OrderType.ONLINE,
        )
    except IntegrityError:
        return None