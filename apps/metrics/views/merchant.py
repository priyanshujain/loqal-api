from decimal import Decimal

from django.db.models import Count, Sum
from django.utils.translation import gettext as _

from api.views import MerchantAPIView
from apps.metrics.services import CreateConsumerRating
from apps.payment.dbapi import get_30days_transactions_merchant


class CreateConsumerRatingAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        CreateConsumerRating(
            merchant=merchant_account, data=self.request_data
        ).handle()
        self.response()


class MerchantMetricsAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        transactions = get_30days_transactions_merchant(
            merchant_account_id=merchant_account.id
        )
        customers = transactions.distinct("payment__order__consumer").count()
        transaction_groups = transactions.values("created_at__day").annotate(
            total=Sum("amount"),
            customers=Count("payment__order__consumer", distinct=True),
        )
        return self.response(
            {
                "customers": customers,
                "total": transactions.aggregate(total=Sum("amount"))["total"]
                or Decimal(0.0),
                "daily_sales": transaction_groups,
            }
        )
