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

            # Ensure CORS is configured for browser access in dev
            try:
                self._ensure_bucket_cors()
            except Exception:
                # Do not fail health because of CORS misconfig
                pass

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

    def generate_presigned_upload_url(self, s3_key: str, content_type: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for uploading a file to S3

        Args:
            s3_key: The S3 key (path) where the file will be stored
            content_type: MIME type of the file
            expires_in: URL expiration time in seconds (default: 1 hour)

        Returns:
            Presigned URL string or None if failed
        """
        try:
            presigned_url = self.client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self._bucket_name,
                    'Key': s3_key,
                    'ContentType': content_type
                },
                ExpiresIn=expires_in,
                HttpMethod='PUT'
            )
            # If a public endpoint is configured, rewrite the hostname so the browser can reach MinIO
            public_base = settings.s3_public_endpoint_url
            if public_base:
                from urllib.parse import urlparse, urlunparse
                u = urlparse(presigned_url)
                pub = urlparse(public_base)
                u = u._replace(scheme=pub.scheme, netloc=pub.netloc)
                presigned_url = urlunparse(u)
            return presigned_url
        except Exception as e:
            print(f"Error generating presigned upload URL: {e}")
            return None

    def _ensure_bucket_cors(self) -> None:
        """Ensure permissive CORS on the bucket for local dev usage.
        Allows common methods and all origins/headers. Idempotent.

        Note: This is intended for development only.
        """
        cors_config = {
            'CORSRules': [
                {
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
                    'AllowedOrigins': ['*'],
                    'ExposeHeaders': ['ETag', 'x-amz-request-id'],
                    'MaxAgeSeconds': 3000,
                }
            ]
        }
        try:
            # Try to fetch current CORS; if missing, set it
            self.client.get_bucket_cors(Bucket=self._bucket_name)
        # type: ignore[attr-defined]
        except self.client.exceptions.NoSuchCORSConfiguration:
            self.client.put_bucket_cors(
                Bucket=self._bucket_name, CORSConfiguration=cors_config)
        except Exception:
            # If any error, attempt to set regardless
            try:
                self.client.put_bucket_cors(
                    Bucket=self._bucket_name, CORSConfiguration=cors_config)
            except Exception:
                pass

    def generate_presigned_download_url(self, s3_key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for downloading a file from S3

        Args:
            s3_key: The S3 key (path) of the file to download
            expires_in: URL expiration time in seconds (default: 1 hour)

        Returns:
            Presigned URL string or None if failed
        """
        try:
            presigned_url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self._bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expires_in
            )
            # If a public endpoint is configured, rewrite the hostname so the browser can reach MinIO
            public_base = settings.s3_public_endpoint_url
            if public_base:
                from urllib.parse import urlparse, urlunparse
                u = urlparse(presigned_url)
                pub = urlparse(public_base)
                u = u._replace(scheme=pub.scheme, netloc=pub.netloc)
                presigned_url = urlunparse(u)
            return presigned_url
        except Exception as e:
            print(f"Error generating presigned download URL: {e}")
            return None

    def delete_file(self, s3_key: str) -> bool:
        """
        Delete a file from S3

        Args:
            s3_key: The S3 key (path) of the file to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_object(Bucket=self._bucket_name, Key=s3_key)
            return True
        except Exception as e:
            print(f"Error deleting file from S3: {e}")
            return False

    def file_exists(self, s3_key: str) -> bool:
        """
        Check if a file exists in S3

        Args:
            s3_key: The S3 key (path) to check

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.client.head_object(Bucket=self._bucket_name, Key=s3_key)
            return True
        except ClientError:
            return False


# Global S3 client instance
s3_client = S3Client()
