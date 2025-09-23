import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "LabelLoop API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # S3/MinIO Configuration
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "False").lower() == "true"

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    @property
    def s3_endpoint_url(self) -> str:
        return f"{'https' if self.MINIO_SECURE else 'http'}://{self.MINIO_ENDPOINT}"


settings = Settings()
