from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile

from app.core.config import settings


def upload_file(file: UploadFile) -> str | None:
    try:
        client = boto3.client(
            service_name="s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
        )
        extension = file.filename.split(".")[-1] if "." in file.filename else ""
        if not extension:
            raise ValueError
        file_name = f"{uuid4().hex}.{extension}"
        client.upload_fileobj(file.file, settings.AWS_S3_BUCKET_NAME, file_name)
        return f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"

    except (BotoCoreError, ClientError):
        return None
