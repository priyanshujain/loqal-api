from django.utils.translation import gettext as _
from django.utils.translation import ungettext

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.marketing.dbapi import create_campaign, get_campaign_by_title
from apps.marketing.validators import CreateCampaignValidator


class CreateCampaign(ServiceBase):
    def __init__(self, data):
        self.data = data

    def handle(self):
        data = self.validate()
        return self._factory_campaign(data=data)

    def validate(self):
        data = run_validator(CreateCampaignValidator, data=self.data)
        title = data["title"]
        campaign = get_campaign_by_title(title=title)
        if campaign:
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _("A campaign already exists with this name.")
                    )
                }
            )
        return data

    def _factory_campaign(self, data):
        return create_campaign(
            title=data["title"],
            short_description=data["short_description"],
            content=data["content"],
            starts_at=data["starts_at"],
            ends_at=data["ends_at"],
            target_amount=data["target_amount"],
        )
