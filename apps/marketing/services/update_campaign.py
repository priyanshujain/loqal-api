from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.marketing.dbapi import get_campaign_by_title, update_campaign
from apps.marketing.validators import CreateCampaignValidator


class UpdateCampaign(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        data = self.validate()
        self._update_campaign(data=data)

    def validate(self):
        data = run_validator(CreateCampaignValidator, data=self.data)
        title = data["title"]
        campaign = get_campaign_by_title(title=title)
        if not campaign:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("Campaign does not exist with this name.")
                    )
                }
            )
        data["campaign"] = campaign
        return data

    def _update_campaign(self, data):
        return update_campaign(
            campaign_id=data["campaign"].id,
            title=data["title"],
            short_description=data["short_description"],
            content=data["content"],
            starts_at=data["starts_at"],
            ends_at=data["ends_at"],
            target_amount=data["target_amount"],
        )
