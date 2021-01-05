import base64
import logging
import os

import html2text
import magic
from celery import shared_task
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Attachment, ContentId, Disposition,
                                   FileContent, FileName, FileType, Mail)

logger = logging.getLogger("")


@shared_task
def send_email(from_name, to_emails, subject, content, **kwargs):
    DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
    SENDGRID_API_KEY = settings.SENDGRID_API_KEY

    message = Mail(
        from_email=(DEFAULT_FROM_EMAIL, from_name),
        to_emails=to_emails,
        subject=f"[Loqal App]: {subject}",
        html_content=content,
    )
    file_path = kwargs.get("file_path", None)
    if file_path:
        with open(file_path, "rb") as f:
            file_content = f.read()
            file_name = f.name
            f.close()
        
        kwarg_file_name = kwargs.get("file_name", None)
        if kwarg_file_name:
            file_name = kwarg_file_name

        encoded_content = base64.b64encode(file_content).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded_content)
        attachment.file_type = FileType(magic.from_file(file_path, mime=True))
        attachment.file_name = FileName(file_name)
        message.attachment = attachment

    sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
    response = sendgrid_client.send(message)
    if file_path:
        try:
            os.unlink(file_path)
        except Exception:
            pass
    return response



def send_email_async(to_emails, subject, content, **kwargs):
    # if settings.APP_ENV == "local":
    #     h = html2text.HTML2Text()
    #     print("###################### EMAIL START ########################")
    #     print("TO: ", to_emails)
    #     print("SUBJECT: ", subject)
    #     print("CONTENT: ", h.handle(content))
    #     print("###################### EMAIL END ##########################")
    #     return

    file_path = kwargs.get("file_path", None)
    file_name = kwargs.get("file_name", None)
    if file_path:
        send_email.delay(
            from_name=settings.EMAIL_SENDER_NAME,
            to_emails=to_emails,
            subject=subject,
            content=content,
            file_path=file_path,
            file_name=file_name,
        )
    else:
        send_email.delay(
            from_name=settings.EMAIL_SENDER_NAME,
            to_emails=to_emails,
            subject=subject,
            content=content,
            file_name=file_name
        )
