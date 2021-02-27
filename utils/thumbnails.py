import logging

from versatileimagefield.image_warmer import VersatileImageFieldWarmer

logger = logging.getLogger(__name__)


def create_thumbnails(pk, model, size_set, image_attr=None):
    instance = model.objects.get(pk=pk)
    if not image_attr:
        image_attr = "image"
    image_instance = getattr(instance, image_attr)
    if image_instance.name == "":
        # There is no file, skip processing
        return
    warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set=size_set,
        image_attr=image_attr,
    )
    logger.info("Creating thumbnails for  %s", pk)
    num_created, failed_to_create = warmer.warm()
    if num_created:
        logger.info("Created %d thumbnails", num_created)
    if failed_to_create:
        logger.error(
            "Failed to generate thumbnails", extra={"paths": failed_to_create}
        )


import re
import warnings

from django.conf import settings


# cache available sizes at module level
def get_available_sizes():
    rendition_sizes = {}
    keys = settings.VERSATILEIMAGEFIELD_RENDITION_KEY_SETS
    for dummy_size_group, sizes in keys.items():
        rendition_sizes[dummy_size_group] = {size for _, size in sizes}
    return rendition_sizes


AVAILABLE_SIZES = get_available_sizes()


def get_available_sizes_by_method(method, rendition_key_set):
    sizes = []
    for available_size in AVAILABLE_SIZES[rendition_key_set]:
        available_method, avail_size_str = available_size.split("__")
        if available_method == method:
            sizes.append(min([int(s) for s in avail_size_str.split("x")]))
    return sizes


def get_thumbnail_size(size, method, rendition_key_set):
    """Return the closest larger size if not more than 2 times larger.

    Otherwise, return the closest smaller size
    """
    on_demand = settings.VERSATILEIMAGEFIELD_SETTINGS[
        "create_images_on_demand"
    ]
    if isinstance(size, int):
        size_str = "%sx%s" % (size, size)
    else:
        size_str = size
    size_name = "%s__%s" % (method, size_str)
    if size_name in AVAILABLE_SIZES[rendition_key_set] or on_demand:
        return size_str
    avail_sizes = sorted(
        get_available_sizes_by_method(method, rendition_key_set)
    )
    larger = [x for x in avail_sizes if size < x <= size * 2]
    smaller = [x for x in avail_sizes if x <= size]

    if larger:
        return "%sx%s" % (larger[0], larger[0])
    elif smaller:
        return "%sx%s" % (smaller[-1], smaller[-1])
    msg = (
        "Thumbnail size %s is not defined in settings "
        "and it won't be generated automatically" % size_name
    )
    warnings.warn(msg)
    return None


def get_thumbnail(image_file, rendition_key_set, method, size=None):
    if image_file:
        if not size:
            return image_file.url
        used_size = get_thumbnail_size(size, method, rendition_key_set)

        try:
            thumbnail = getattr(image_file, method)[used_size]
        except Exception:
            logger.exception(
                "Thumbnail fetch failed",
                extra={"image_file": image_file, "size": size},
            )
        else:
            return thumbnail.url
        return image_file.url
    return None
