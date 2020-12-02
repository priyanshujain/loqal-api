from celery import Task

from apps.payment.services import TransactionStatusUpdate
from config.celery import app


class TransactionStatusUpdateTask(Task):
    name = "transaction_status_update"

    def run(self, account_id):
        service = TransactionStatusUpdate(account_id=account_id)
        service.execute()


app.tasks.register(TransactionStatusUpdateTask)
