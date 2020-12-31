from django.db.utils import IntegrityError

from apps.support.models import SupportTicket


def create_support_ticket(user_id, message):
    try:
        return SupportTicket.objects.create(user_id=user_id, message=message)
    except IntegrityError:
        return None


def get_support_tickets(user_id):
    return SupportTicket.objects.filter(user_id=user_id)
