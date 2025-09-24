from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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


class ImageCreate(ImageBase):
    """Schema for creating a new image"""
    dataset_id: int = Field(..., gt=0,
                            description="ID of the dataset this image belongs to")


class ImageUpdate(BaseModel):
    """Schema for updating an image"""
    filename: Optional[str] = Field(None, min_length=1, max_length=255)
    width: Optional[int] = Field(None, gt=0)
    height: Optional[int] = Field(None, gt=0)


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
