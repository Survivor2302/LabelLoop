from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DatasetBase(BaseModel):
    """Base dataset schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255,
                      description="Dataset name")
    description: Optional[str] = Field(
        None, max_length=1000, description="Dataset description")


class DatasetCreate(DatasetBase):
    """Schema for creating a new dataset"""
    label_names: List[str] = Field(
        default_factory=list, description="List of label names to associate with the dataset")


class DatasetUpdate(BaseModel):
    """Schema for updating a dataset"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


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


class DatasetWithLabels(Dataset):
    """Schema for dataset with associated labels"""
    labels: List["Label"] = Field(
        default_factory=list, description="Labels in dataset")

    class Config:
        from_attributes = True


class DatasetDetail(BaseModel):
    """Schema for detailed dataset response with counts"""
    id: int = Field(..., description="Dataset ID")
    name: str = Field(..., description="Dataset name")
    description: Optional[str] = Field(None, description="Dataset description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    image_count: int = Field(..., description="Number of images in dataset")
    annotation_count: int = Field(...,
                                  description="Number of annotations in dataset")
    label_count: int = Field(...,
                             description="Number of labels linked to dataset")
