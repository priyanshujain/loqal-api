from apps.box.models import BoxFile


def get_boxfile(boxfile_id, account_id=None):
    boxfile_qs = BoxFile.objects.filter(id=boxfile_id)
    if account_id:
        boxfile_qs = boxfile_qs.filter(account_id=account_id)
    if boxfile_qs.exists():
        return boxfile_qs.first()
    return None


def create_boxfile(
    account_id,
    file_name,
    file_path,
    content_type,
    encryption_key,
    document_type,
):
    return BoxFile.objects.create(
        account_id=account_id,
        file_name=file_name,
        file_path=file_path,
        content_type=content_type,
        encryption_key=encryption_key,
        document_type=document_type,
    )
