from decimal import Decimal

from django.db.models import Sum
from django.utils.translation import gettext as _

from api.views import ConsumerAPIView
from apps.account.dbapi import get_merchant_account
from apps.metrics.dbapi import get_merchant_to_consumer_rating
from apps.metrics.services import CreateSocialShare
from apps.payment.dbapi import get_30days_transactions_consumer, transaction


class CreateSocialShareAPI(ConsumerAPIView):
    def post(self, request):
        consumer_account = request.consumer_account
        CreateSocialShare(
            consumer=consumer_account, data=self.request_data
        ).handle()
        self.response()


class ConsumerMetricsAPI(ConsumerAPIView):
    def get(self, request):
        consumer_account = request.consumer_account
        transactions = get_30days_transactions_consumer(
            consumer_account_id=consumer_account.id
        )
        transaction_groups = transactions.values(
            "payment__order__merchant"
        ).annotate(total=Sum("amount"))
        category_transactions = {}
        for transaction_group in transaction_groups:
            merchant_id = transaction_group["payment__order__merchant"]
            merchant = get_merchant_account(merchant_id=merchant_id)
            category = merchant.category.category
            if category in category_transactions:
                category_transactions[category] += transaction_group["total"]
            else:
                category_transactions[category] = transaction_group["total"]
        return self.response(
            {
                "count": transactions.count(),
                "total": transactions.aggregate(total=Sum("amount"))["total"]
                or Decimal(0.0),
                "thanks_received": get_merchant_to_consumer_rating(
                    consumer_id=consumer_account.id
                ).count(),
                "category_transactions_total": category_transactions,
            }
        )
