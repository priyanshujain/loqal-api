from apps.box.models import BoxFile


def get_boxfile(boxfile_id):
    try:
        return BoxFile.objects.get(id=boxfile_id)
    except BoxFile.DoesNotExist:
        return None


def create_boxfile(
    file_name,
    file_path,
    content_type,
    encryption_key,
    document_type,
):
    return BoxFile.objects.create(
        file_name=file_name,
        file_path=file_path,
        content_type=content_type,
        encryption_key=encryption_key,
        document_type=document_type,
    )
