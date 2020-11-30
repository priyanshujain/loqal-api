import os


def validate_image_data(image_obj):
    suffix = os.path.splitext(image_obj.name)[-1].lower()
    if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
        return False

    return True
