import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional
from .config import settings


class S3Client:
    def __init__(self):
        self._client: Optional[boto3.client] = None
        self._bucket_name = settings.MINIO_BUCKET

    @property
    def client(self) -> boto3.client:
        """Lazy initialization of S3 client"""
        if self._client is None:
            self._client = boto3.client(
                's3',
                endpoint_url=settings.s3_endpoint_url,
                aws_access_key_id=settings.MINIO_ACCESS_KEY,
                aws_secret_access_key=settings.MINIO_SECRET_KEY,
                region_name='us-east-1'  # MinIO doesn't care about region
            )
        return self._client

    def is_configured(self) -> bool:
        """Check if S3 configuration is complete"""
        return all([
            settings.MINIO_ENDPOINT,
            settings.MINIO_ACCESS_KEY,
            settings.MINIO_SECRET_KEY
        ])

    def test_connection(self) -> tuple[bool, str, float]:
        """
        Test S3 connection and return (success, message, latency_ms)
        """
        if not self.is_configured():
            return False, "S3 configuration is incomplete", 0.0

        try:
            import time
            start_time = time.perf_counter()

            # Test connection by listing buckets
            self.client.list_buckets()

            # Test bucket access
            self.client.head_bucket(Bucket=self._bucket_name)

            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return True, "S3 connection successful", latency_ms

        except NoCredentialsError:
            return False, "S3 credentials are invalid", 0.0
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            if error_code == 'NoSuchBucket':
                return False, f"Bucket '{self._bucket_name}' does not exist", 0.0
            elif error_code == 'Forbidden':
                return False, "S3 access forbidden - check credentials", 0.0
            else:
                return False, f"S3 error: {error_code}", 0.0
        except Exception as e:
            return False, f"S3 connection failed: {str(e)}", 0.0


# Global S3 client instance
s3_client = S3Client()
