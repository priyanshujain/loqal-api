from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import LoggedInAPIView
from apps.box.models import BoxFile
from apps.box.responses import BoxFileResponse
from apps.box.shortcut import fix_mimetype_file, validate_file_format
from apps.box.tasks import get_file_from_fss, store_file_to_fss
from apps.box.validators import BoxFileForm


class FileAPI(LoggedInAPIView):
    def validate_form(self, form):
        if not form.is_valid():
            return (
                None,
                ValidationError(
                    {
                        "detail": ErrorDetail(
                            _("Invalid data. Please try again.")
                        )
                    }
                ),
            )
        data = form.cleaned_data
        return data, None


class CreateFileAPI(FileAPI):
    def post(self, request):
        form = BoxFileForm(request.POST, request.FILES)
        data, error = self.validate_form(form)
        if error:
            raise error

        source_file = data["source_file"]
        source_file = fix_mimetype_file(source_file)
        if not validate_file_format(source_file):
            raise ValidationError(
                {
                    "source_file": [
                        ErrorDetail(
                            _(
                                "Unsupported file format. Please make sure "
                                "you use .jpg, .jpeg, .pdf or .png file."
                            )
                        )
                    ]
                }
            )

        gcs_file = store_file_to_fss(
            source_file, source_file.name, source_file.content_type
        )

        boxfile = BoxFile.objects.create(
            file_name=source_file.name,
            file_path=gcs_file["file_name"],
            content_type=gcs_file["content_type"],
            encryption_key=gcs_file["encryption_key"],
            document_type=data["document_type"],
        )
        return self.response({"id": boxfile.id, "file_name": source_file.name})


class FetchFileUrlAPI(LoggedInAPIView):
    def get(self, request):
        # TODO: replace id with u_id
        box_id = request.GET.get("box_id", None)
        if not box_id:
            raise ValidationError(
                {"box_id": [ErrorDetail(_("box_id parameter is required."))]}
            )

        try:
            box_id = int(box_id)
        except ValueError:
            raise ValidationError(
                {"box_id": [ErrorDetail(_("Invalid box_id."))]}
            )

        try:
            box_file = BoxFile.objects.get(pk=box_id)
        except BoxFile.DoesNotExist:
            raise ValidationError(
                {"box_id": [ErrorDetail(_("Invalid box_id."))]}
            )

        box_file_data = BoxFileResponse(box_file).data
        box_file_data["signed_url"] = get_file_from_fss(
            file_path=box_file.file_path,
            encryption_key=box_file.encryption_key,
        )
        return self.response(box_file_data)
