from decimal import Decimal

from django.db.models import Count, Max, Sum
from django.utils.translation import gettext as _

from api.views import MerchantAPIView, PosStaffAPIView
from apps.metrics.notifications import SendConsumerRatingNotification
from apps.metrics.services import CreateConsumerRating
from apps.payment.dbapi import get_30days_transactions_merchant
from utils.dates import datetime_format


class CreateConsumerRatingAPI(MerchantAPIView):
    def post(self, request):
        merchant_account = request.merchant_account
        rating = CreateConsumerRating(
            merchant=merchant_account, data=self.request_data
        ).handle()
        SendConsumerRatingNotification(
            user_id=rating.consumer.user.id,
            data={
                "merchant_name": merchant_account.profile.full_name,
                "created_at": datetime_format(rating.created_at),
                "transaction": {
                    "created_at": datetime_format(
                        rating.transaction.created_at
                    )
                },
            },
        ).send()
        return self.response()


class CreatePosConsumerRatingAPI(CreateConsumerRatingAPI, PosStaffAPIView):
    pass


class MerchantMetricsAPI(MerchantAPIView):
    def get(self, request):
        merchant_account = request.merchant_account
        transactions = get_30days_transactions_merchant(
            merchant_account_id=merchant_account.id
        )
        customers = transactions.distinct("payment__order__consumer").count()
        transaction_groups = transactions.values("created_at__day").annotate(
            date=Max("created_at"),
            total=Sum("amount"),
            customers=Count("payment__order__consumer", distinct=True),
        )
        return self.response(
            {
                "customers": customers,
                "total": transactions.aggregate(total=Sum("amount"))["total"]
                or Decimal(0.0),
                "count": transactions.aggregate(count=Count("id"))["count"]
                or 0,
                "daily_sales": transaction_groups,
            }
        )
