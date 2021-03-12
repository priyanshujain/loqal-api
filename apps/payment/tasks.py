from celery import shared_task

from apps.notification.dbapi import get_staff_payment_notifications
from apps.payment.dbapi import get_payment_by_id
from apps.payment.notifications.email import SendPaymentCapturedEmail
from apps.payment.notifications.sms import SendPaymentCapturedSMS


@shared_task
def create_staff_payment_notification(payment_id):
    payment = get_payment_by_id(payment_id=payment_id)
    if not payment:
        return
    merchant = payment.order.merchant
    staff_notifications = get_staff_payment_notifications(
        merchant_id=merchant.id
    )
    for notification_setting in staff_notifications:
        staff_user = notification_setting.staff.user
        if notification_setting.sms_enabled:
            SendPaymentCapturedSMS(
                payment=payment,
                phone_number=staff_user.phone_number,
                phone_number_country=staff_user.phone_number_country,
            ).send()
        if notification_setting.email_enabled:
            SendPaymentCapturedEmail(
                payment=payment, email=staff_user.email
            ).send()
