from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DatasetStatus(str, Enum):
    """Status of a dataset"""
    CREATING = "creating"
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"


class DatasetBase(BaseModel):
    """Base dataset schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255,
                      description="Dataset name")
    description: Optional[str] = Field(
        None, max_length=1000, description="Dataset description")
    status: DatasetStatus = Field(
        default=DatasetStatus.CREATING, description="Dataset status")


class DatasetCreate(DatasetBase):
    """Schema for creating a new dataset"""
    pass


class DatasetUpdate(BaseModel):
    """Schema for updating a dataset"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[DatasetStatus] = None


class Dataset(DatasetBase):
    """Schema for dataset response"""
    id: int = Field(..., description="Dataset ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    image_count: int = Field(
        default=0, description="Number of images in dataset")

    class Config:
        from_attributes = True


class DatasetWithImages(Dataset):
    """Schema for dataset with associated images"""
    images: List["Image"] = Field(
        default_factory=list, description="Images in dataset")

    class Config:
        from_attributes = True
