from django.utils.translation import gettext as _

from api.exceptions import ErrorDetail, ValidationError
from api.views import LoggedInAPIView
from apps.box.models import BoxFile
from apps.box.serializers import BoxFileForm, BoxFileSerializer
from apps.box.shortcut import validate_file_format
from apps.box.tasks import get_file_from_gcs, store_file_to_gcs


class FileAPI(LoggedInAPIView):
    def validate_form(self, form):
        if not form.is_valid():
            return (
                None,
                ValidationError({"detail": ErrorDetail(_("Invalid data."))}),
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
        if not validate_file_format(source_file):
            raise ValidationError(
                {"source_file": [ErrorDetail(_("Unsupported file format."))]}
            )

        gcs_file = store_file_to_gcs(
            source_file, source_file.name, source_file.content_type
        )

        boxfile = BoxFile.objects.create(
            account=request.account,
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
        # TODO: apply file permission check for account
        box_id = request.GET.get("box_id", None)
        if not box_id:
            raise ValidationError(
                {"box_id": [ErrorDetail(_("box_id parameter is required."))]}
            )

        try:
            box_id = int(box_id)
        except ValueError:
            raise ValidationError(
                {"box_id": [ErrorDetail(_("Invalid box id."))]}
            )

        try:
            box_file = BoxFile.objects.get(pk=box_id)
        except BoxFile.DoesNotExist:
            raise ValidationError(
                {"box_id": [ErrorDetail(_("Invalid box_id."))]}
            )

        box_file_data = BoxFileSerializer(box_file).data
        box_file_data["signed_url"] = get_file_from_gcs(box_file_data)
        del box_file_data["encryption_key"]
        return self.response(box_file_data)
