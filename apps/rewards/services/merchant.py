from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import ungettext

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from api.services import ServiceBase
from apps.rewards.dbapi import (create_loyalty_program,
                                get_current_loyalty_program,
                                update_loyalty_program)
from apps.rewards.options import LoyaltyParameters
from apps.rewards.validators import (CreateLoyaltyProgramValidator,
                                     EditLoyaltyProgramValidator)
from utils.dates import dt_add_months


class CreateLoyaltyProgram(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self.validate()
        return self._factory_loyalty_program(data=data)

    def validate(self):
        loyalty_program = get_current_loyalty_program(
            merchant_id=self.merchant.id
        )
        if loyalty_program:
            raise ValidationError(
                {
                    "detail": _(
                        "You already have a loyalty active. "
                        "Please deactivate it to setup a new loyalty program."
                    )
                }
            )
        data = run_validator(CreateLoyaltyProgramValidator, data=self.data)
        return data

    def _factory_loyalty_program(self, data):
        program_start_date = timezone.now()
        program_end_date = None
        if data.get("program_months"):
            program_end_date = dt_add_months(
                dt=program_start_date, months=data["program_months"]
            )
        min_total_purchase = data.get("min_total_purchase")
        min_visits = data.get("min_visits")
        if not (min_total_purchase or min_visits):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Please select at least on option out "
                            "of number of visits/ Total amount spent."
                        )
                    )
                }
            )
        return create_loyalty_program(
            merchant_id=self.merchant.id,
            loyalty_parameter=data["loyalty_parameter"],
            program_start_date=program_start_date,
            program_end_date=program_end_date,
            reward_value_type=data["reward_value_type"],
            reward_value=data["reward_value"],
            min_total_purchase=min_total_purchase,
            min_visits=min_visits,
        )


class EditLoyaltyProgram(ServiceBase):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def handle(self):
        data = self.validate()
        self._edit_loyalty_program(data=data)

    def validate(self):
        loyalty_program = get_current_loyalty_program(
            merchant_id=self.merchant.id
        )
        if not loyalty_program:
            raise ValidationError(
                {
                    "detail": _(
                        "Loyalty program does not exist. "
                        "Please create a new loyalty program."
                    )
                }
            )
        data = run_validator(EditLoyaltyProgramValidator, data=self.data)
        data["loyalty_program"] = loyalty_program
        return data

    def _edit_loyalty_program(self, data):
        loyalty_program = data["loyalty_program"]
        loyalty_parameter = loyalty_program.loyalty_parameter
        program_start_date = loyalty_program.program_start_date
        program_end_date = loyalty_program.program_end_date
        if data.get("program_months"):
            program_end_date = dt_add_months(
                dt=program_start_date, months=data["program_months"]
            )
        min_total_purchase = loyalty_program.min_total_purchase
        if data.get("min_total_purchase"):
            min_total_purchase = data.get("min_total_purchase")

        min_visits = loyalty_program.min_visits
        if data.get("min_visits"):
            min_visits = data.get("min_visits")

        if not (min_total_purchase or min_visits):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Please select at least on option out "
                            "of number of visits/ Total amount spent."
                        )
                    )
                }
            )

        if (
            loyalty_parameter == LoyaltyParameters.NUMBER_OF_VISITS
            and not min_visits
        ) or (
            loyalty_parameter == LoyaltyParameters.AMOUNT_SPENT
            and not min_total_purchase
        ):
            raise ValidationError(
                {
                    "detail": ErrorDetail(
                        _(
                            "Please select the value according to "
                            "loyalty program type."
                        )
                    )
                }
            )
        update_loyalty_program(
            merchant_id=self.merchant.id,
            loyalty_parameter=loyalty_parameter,
            program_start_date=program_start_date,
            program_end_date=program_end_date,
            reward_value_type=data["reward_value_type"],
            reward_value=data["reward_value"],
            min_total_purchase=min_total_purchase,
            min_visits=min_visits,
        )
