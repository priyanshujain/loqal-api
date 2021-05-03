from apps.payment.models import Payment


def get_pos_payments(register_id):
    return Payment.objects.filter(register_id=register_id).order_by(
        "-created_at"
    )[:5]
