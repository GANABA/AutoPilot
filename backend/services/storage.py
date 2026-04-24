import boto3
from botocore.config import Config
from config import get_settings

settings = get_settings()

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = boto3.client(
            "s3",
            endpoint_url=settings.cloudflare_r2_endpoint,
            aws_access_key_id=settings.cloudflare_r2_access_key,
            aws_secret_access_key=settings.cloudflare_r2_secret_key,
            config=Config(signature_version="s3v4"),
            region_name="auto",
        )
    return _client


async def upload_file(content: bytes, key: str, content_type: str) -> str:
    client = _get_client()
    client.put_object(
        Bucket=settings.cloudflare_r2_bucket,
        Key=key,
        Body=content,
        ContentType=content_type,
    )
    return f"{settings.cloudflare_r2_endpoint}/{settings.cloudflare_r2_bucket}/{key}"
