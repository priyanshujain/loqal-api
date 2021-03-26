from celery import shared_task

from apps.user.models import User
from utils.thumbnails import create_thumbnails


@shared_task
def create_user_avatar_thumbnails(user_id):
    """Create thumbnails for user avatar."""
    create_thumbnails(
        pk=user_id, model=User, size_set="user_avatars", image_attr="avatar"
    )
