from django.contrib.postgres.search import TrigramSimilarity

from apps.reference.models import City, Country, RegionState, ZipCode


def get_all_countries():
    return Country.objects.all()


def partial_search_city(country_code, partial_city_name):
    city_qs = (
        City.objects.filter(country_code=country_code)
        .annotate(
            similarity=TrigramSimilarity("name", partial_city_name),
        )
        .filter(similarity__gt=0.3)
        .order_by("-similarity")
    )
    return [city_obj.name for city_obj in city_qs]


def get_country(country_code):
    try:
        return Country.objects.get(iso_code=country_code)
    except Country.DoesNotExist:
        return None


def get_region_states(country_code):
    return RegionState.objects.filter(country_code=country_code)


def get_zipcode(code):
    try:
        return ZipCode.objects.get(code=code)
    except ZipCode.DoesNotExist:
        return None
