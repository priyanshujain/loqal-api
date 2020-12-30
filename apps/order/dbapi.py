from django.db.utils import IntegrityError

from apps.order.models import Order
from apps.order.options import OrderType


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


def get_order_by_id(order_id, merchant_id):
    """
    get an order
    """
    try:
        return Order.objects.get(
            merchant_id=merchant_id,
            id=order_id,
        )
    except Order.DoesNotExist:
        return None
