from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ImageStatus(str, Enum):
    """Image upload status"""
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    ERROR = "error"


class ImageBase(BaseModel):
    """Base image schema with common fields"""
    filename: str = Field(..., min_length=1, max_length=255,
                          description="Original filename")
    s3_key: str = Field(..., min_length=1, description="S3 object key")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of the image")
    width: Optional[int] = Field(
        None, gt=0, description="Image width in pixels")
    height: Optional[int] = Field(
        None, gt=0, description="Image height in pixels")
    status: ImageStatus = Field(
        default=ImageStatus.UPLOADING, description="Upload status")


class ImageCreate(ImageBase):
    """Schema for creating a new image"""
    dataset_id: int = Field(..., gt=0,
                            description="ID of the dataset this image belongs to")


class ImageUpdate(BaseModel):
    """Schema for updating an image"""
    filename: Optional[str] = Field(None, min_length=1, max_length=255)
    width: Optional[int] = Field(None, gt=0)
    height: Optional[int] = Field(None, gt=0)
    status: Optional[ImageStatus] = None


class Image(ImageBase):
    """Schema for image response"""
    id: int = Field(..., description="Image ID")
    dataset_id: int = Field(..., description="Dataset ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class ImageWithDataset(Image):
    """Schema for image with associated dataset"""
    dataset: "Dataset" = Field(...,
                               description="Dataset this image belongs to")

    class Config:
        from_attributes = True


# Schemas for presigned URL workflow
class ImageUploadRequest(BaseModel):
    """Schema for requesting image upload"""
    filename: str = Field(..., min_length=1, max_length=255,
                          description="Original filename")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of the image")


class ImageUploadResponse(BaseModel):
    """Schema for image upload response with presigned URL"""
    image_id: int = Field(..., description="Created image ID")
    upload_url: str = Field(..., description="Presigned URL for upload")
    s3_key: str = Field(..., description="S3 key where file will be stored")
    expires_in: int = Field(
        default=3600, description="URL expiration time in seconds")


class ImageUploadBatchRequest(BaseModel):
    """Schema for batch image upload request"""
    files: List[ImageUploadRequest] = Field(...,
                                            description="List of files to upload")


class ImageUploadBatchResponse(BaseModel):
    """Schema for batch image upload response"""
    uploads: List[ImageUploadResponse] = Field(
        ..., description="List of upload URLs")


class ImageConfirmUploadRequest(BaseModel):
    """Schema for confirming successful uploads"""
    image_ids: List[int] = Field(...,
                                 description="List of successfully uploaded image IDs")


class ImageWithDownloadUrl(Image):
    """Schema for image with presigned download URL"""
    download_url: Optional[str] = Field(
        None, description="Presigned URL for downloading the image")
    url_expires_in: Optional[int] = Field(
        None, description="URL expiration time in seconds")

    class Config:
        from_attributes = True


class ImageListResponse(BaseModel):
    """Schema for paginated image list response"""
    total: int = Field(..., description="Total number of images")
    items: List[Image] = Field(..., description="List of images")


class ImageWithUrlListResponse(BaseModel):
    """Schema for paginated image list response with download URLs"""
    total: int = Field(..., description="Total number of images")
    items: List[ImageWithDownloadUrl] = Field(
        ..., description="List of images with download URLs")
