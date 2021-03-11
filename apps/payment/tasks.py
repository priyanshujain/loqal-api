from celery import shared_task

from api.views import merchant
from apps.notification.dbapi import get_staff_payment_notifications
from apps.payment.dbapi import get_payment_by_id
from apps.payment.notifications.email import SendPaymentCapturedEmail
from apps.payment.notifications.sms import SendPaymentCapturedSMS
import logging

logger = logging.getLogger(__name__)

@shared_task
def create_staff_payment_notification(payment_id):
    logger.warning(f"Payment id {payment_id}")
    payment = get_payment_by_id(payment_id=payment_id)
    logger.warning(f"Payment {payment.id}")
    if not payment:
        return
    merchant = payment.order.merchant
    logger.warning(f"merchant {merchant.id}")
    staff_notifications = get_staff_payment_notifications(
        merchant_id=merchant.id
    )
    logger.warning(f"staff notifications {staff_notifications.count()}")
    for notification_setting in staff_notifications:
        staff_user = notification_setting.staff.user
        if notification_setting.sms_enabled:
            logger.warning(f"SMS")
            SendPaymentCapturedSMS(
                payment=payment,
                phone_number=staff_user.phone_number,
                phone_number_country=staff_user.phone_number_country,
            ).send()
        if notification_setting.email_enabled:
            logger.warning(f"Email")
            SendPaymentCapturedEmail(
                payment=payment, email=staff_user.email
            ).send()
