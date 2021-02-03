from django.db.models import Q
from django.db.utils import IntegrityError
from django.utils.timezone import now

from apps.marketing.models import Campaign


def create_campaign(
    title,
    short_description,
    content,
    starts_at,
    ends_at,
    target_amount,
):
    try:
        return Campaign.objects.create(
            title=title,
            short_description=short_description,
            content=content,
            starts_at=starts_at,
            ends_at=ends_at,
            target_amount=target_amount,
        )
    except IntegrityError:
        return None


def update_campaign(
    campaign_id,
    title,
    short_description,
    content,
    starts_at,
    ends_at,
    target_amount,
):
    Campaign.objects.filter(id=campaign_id).update(
        title=title,
        short_description=short_description,
        content=content,
        starts_at=starts_at,
        ends_at=ends_at,
        target_amount=target_amount,
    )


def get_active_campaigns():
    current_datetime = now()
    return Campaign.objects.filter(is_active=True).filter(
        Q(starts_at__lte=current_datetime) & Q(ends_at__gte=current_datetime)
    )


def get_campaign_by_title(title):
    try:
        return Campaign.objects.get(title=title)
    except Campaign.DoesNotExist:
        return None


def get_all_campaigns():
    return Campaign.objects.all()
