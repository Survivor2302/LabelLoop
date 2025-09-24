from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LabelBase(BaseModel):
    """Base label schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255,
                      description="Label name")


class LabelCreate(LabelBase):
    """Schema for creating a new label"""
    dataset_id: int = Field(..., gt=0,
                            description="ID of the dataset this label belongs to")


class LabelUpdate(BaseModel):
    """Schema for updating a label"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class Label(LabelBase):
    """Schema for label response"""
    id: int = Field(..., description="Label ID")
    dataset_id: int = Field(..., description="Dataset ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class LabelWithDataset(Label):
    """Schema for label with associated dataset"""
    dataset: "Dataset" = Field(...,
                               description="Dataset this label belongs to")

    class Config:
        from_attributes = True


class LabelWithAnnotations(Label):
    """Schema for label with associated annotations"""
    annotations: List["Annotation"] = Field(
        default_factory=list, description="Annotations using this label")

    class Config:
        from_attributes = True
