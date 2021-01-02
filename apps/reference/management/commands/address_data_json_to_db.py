import json
import os

from django.apps import apps
from django.core.management.base import BaseCommand

from apps.reference.models import City, Country, RegionState


class Command(BaseCommand):
    def handle(self, *args, **options):
        DATA_DIR = "data/static"
        with open(os.path.join(DATA_DIR, "countries.json")) as f:
            countries = json.load(f)

        for country in countries:
            Country.objects.get_or_create(
                name=country["name"], iso_code=country["code"]
            )
            country_path = os.path.join(DATA_DIR, "countries", country["code"])
            with open(os.path.join(country_path, "cities.json")) as f:
                cities = json.load(f)
            for city in cities:
                City.objects.get_or_create(
                    name=city["city_name"], country_code=country["code"]
                )

            with open(os.path.join(country_path, "regions.json")) as f:
                regions = json.load(f)
            for region in regions:
                try:
                    RegionState.objects.get_or_create(
                        name=region["region_name"],
                        region_code=region["region_code"],
                        country_code=country["code"],
                    )
                except Exception as e:
                    print(e, region)
