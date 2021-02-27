from django.utils.translation import gettext as _

from apps.user.serializers import AvatarSerializer
from apps.user.tasks import create_user_avatar_thumbnails


class AddChangeUserAvatar(object):
    def __init__(self, request):
        self.request = request

    def handle(self):
        request = self.request
        serializer = AvatarSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        create_user_avatar_thumbnails.delay(user_id=request.user.id)
