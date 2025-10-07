from pydantic import BaseModel, Field
from typing import Optional, List


class LabelListResponse(BaseModel):
    """Schema for paginated label list response"""
    total: int = Field(..., description="Total number of labels")
    items: List["Label"] = Field(..., description="List of labels")


class LabelBase(BaseModel):
    """Base label schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255,
                      description="Label name")


class LabelCreate(LabelBase):
    """Schema for creating a new label"""
    pass


class Label(LabelBase):
    """Schema for label response"""
    id: int = Field(..., description="Label ID")

    class Config:
        from_attributes = True


class LabelWithDatasets(Label):
    """Schema for label with associated datasets"""
    datasets: List["Dataset"] = Field(
        default_factory=list, description="Datasets using this label")

    class Config:
        from_attributes = True


class LabelWithAnnotations(Label):
    """Schema for label with associated annotations"""
    annotations: List["Annotation"] = Field(
        default_factory=list, description="Annotations using this label")

    class Config:
        from_attributes = True
