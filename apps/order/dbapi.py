from django.db.models import Q
from django.db.utils import IntegrityError

from apps.order.models import Order
from apps.order.options import OrderType
from apps.payment.options import ChargeStatus


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


def create_base_order(merchant_id, consumer_id, amount, order_type):
    """
    Create an order
    """
    try:
        return Order.objects.create(
            merchant_id=merchant_id,
            consumer_id=consumer_id,
            total_net_amount=amount,
            total_amount=amount,
            order_type=order_type,
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


def get_orders_in_period(consumer_id, merchant_id, start_date, end_date):
    return Order.objects.filter(
        consumer_id=consumer_id,
        merchant_id=merchant_id,
        is_paid=True,
        is_rewarded=False,
    ).filter(Q(created_at__gte=start_date) & Q(created_at__lte=end_date))


def get_rewarded_merchant_orders(consumer_id):
    return Order.objects.filter(
        consumer_id=consumer_id,
        is_rewarded=True,
    ).distinct("merchant")
