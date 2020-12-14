import json
import os

from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.provider.models import PaymentProvider
from apps.reference.models import ProviderPopCode, PurposeOfPayment


def file_to_pop_data(filename):
    content = filename.split(".")[0]
    is_high_value = content[7:]
    if is_high_value == "true":
        is_high_value = True
    else:
        is_high_value = False
    return content[:2], content[2:4], content[4:7], is_high_value


class Command(BaseCommand):
    def handle(self, *args, **options):
        DATA_DIR = "data/static/pop"
        payment_provider = PaymentProvider.objects.get(provider_slug="AFEX")
        for file_name in os.listdir(DATA_DIR):
            file_path = os.path.join(DATA_DIR, file_name)
            (
                bene_country_code,
                bank_country_code,
                currency,
                is_high_value,
            ) = file_to_pop_data(file_name)
            clearing_method = "local"
            if is_high_value:
                clearing_method = "swift"
            file_ext = file_name.split(".")[-1]
            if file_ext == "json" and os.stat(file_path).st_size != 0:
                with open(file_path) as f:
                    try:
                        pop_codes = json.load(f)
                        for pop_code in pop_codes:
                            (
                                pop_value,
                                _,
                            ) = PurposeOfPayment.objects.get_or_create(
                                bank_country_code=bank_country_code,
                                beneficiary_country_code=bene_country_code,
                                currency=currency,
                                name=pop_code["Description"],
                                slug=f"{slugify(pop_code['Description'])}_{bene_country_code}_{bank_country_code}_{currency}_{clearing_method}".lower(),
                                clearing_method=clearing_method.upper(),
                            )
                            ProviderPopCode.objects.get_or_create(
                                provider=payment_provider,
                                pop_value=pop_value,
                                code=pop_code["Code"],
                            )

                    except json.JSONDecodeError:
                        print(file_name)
