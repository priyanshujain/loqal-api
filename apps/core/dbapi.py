from django.db.utils import IntegrityError

from apps.core.models import AppMetaData


def create_app_metadata(
    min_allowed_version, new_version, platform, store_url, api_env
):
    try:
        return AppMetaData.objects.create(
            min_allowed_version=min_allowed_version,
            new_version=new_version,
            platform=platform,
            store_url=store_url,
            api_env=api_env,
        )
    except IntegrityError as error:
        print(error)
        return None


def update_app_metadata(
    min_allowed_version, new_version, platform, store_url, api_env
):
    qs = AppMetaData.objects.filter(platform=platform).update(
        min_allowed_version=min_allowed_version,
        new_version=new_version,
        store_url=store_url,
        api_env=api_env,
    )


def get_app_metadata():
    return AppMetaData.objects.all()


def get_platform_app_metadata(platform):
    try:
        return AppMetaData.objects.get(platform=platform)
    except AppMetaData.DoesNotExist:
        return None
