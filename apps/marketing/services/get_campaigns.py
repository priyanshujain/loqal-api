from decimal import Decimal

from django.db.models import Sum
from django.utils.translation import gettext as _
from django.utils.translation import ungettext

from api.services import ServiceBase
from apps.marketing.dbapi import get_active_campaigns
from apps.payment.dbapi import get_transactions_in_period


class GetCampaigns(ServiceBase):
    def __init__(self):
        pass

    def handle(self):
        data = []
        campaigns = get_active_campaigns()
        for campaign in campaigns:
            data.append(
                {
                    "title": campaign.title,
                    "short_description": campaign.short_description,
                    "content": campaign.content,
                    "starts_at": campaign.starts_at,
                    "ends_at": campaign.ends_at,
                    "target_amount": campaign.target_amount,
                    "achieved_amount": get_transactions_in_period(
                        time_from=campaign.starts_at, time_to=campaign.ends_at
                    ).aggregate(total=Sum("amount"))["total"]
                    or Decimal(0.0),
                }
            )
        return data
