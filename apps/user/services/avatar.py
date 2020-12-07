from django.conf import settings
from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.helpers import run_validator
from apps.user.validators import AvatarValidator
from apps.box.dbapi import get_boxfile

__all__ = (
    "AddChangeUserAvatar",
)

ALLOWED_FILE_TYPES = ("image/gif", "image/jpeg", "image/png")


class AddChangeUserAvatar(object):
    def __init__(self, user, data):
        self.data = data
        self.user = user

    def _validate_data(self):
        data =  run_validator(validator=AvatarValidator, data=self.data)
        avatar_file_id = data["avatar_file_id"]
        boxfile  = get_boxfile(boxfile_id=avatar_file_id)
        if not boxfile:
            raise ValidationError({
                "avatar_file_id": ErrorDetail(_("Given file id is not valid."))
            })
        
        if not boxfile.content_type in ALLOWED_FILE_TYPES:
            raise ValidationError({
                "detail": ErrorDetail(_("Given file type is not supported."))
            })
        
        if boxfile.document_type != "avatar":
            raise ValidationError({
                "detail": ErrorDetail(_("Given document type is not valid, it should be avatar for user avatar."))
            })
        return boxfile
    
    def handle(self):
        boxfile = self._validate_data()
        self.user.change_avatar(boxfile=boxfile)