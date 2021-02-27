from django.utils.translation import gettext as _

from api.helpers import run_validator
from apps.merchant.dbapi import create_store_image
from apps.merchant.tasks import create_store_image_thumbnails
from apps.merchant.validators import StoreImageValidator


class AddStoreImage(object):
    def __init__(self, merchant, data):
        self.merchant = merchant
        self.data = data

    def _validate_data(self):
        run_validator(StoreImageValidator, self.data)
        return True

    def handle(self):
        self._validate_data()
        image = self.data["image"]
        alt = self.data.get("alt", "")
        store_image = create_store_image(
            merchant_id=self.merchant.id, image=image, alt=alt
        )
        create_store_image_thumbnails.delay(image_id=store_image.id)
        return store_image
