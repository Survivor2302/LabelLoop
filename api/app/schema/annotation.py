from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnnotationBase(BaseModel):
    """Base annotation schema with common fields"""
    bbox_xmin: Optional[int] = Field(
        None, ge=0, description="Bounding box x minimum")
    bbox_ymin: Optional[int] = Field(
        None, ge=0, description="Bounding box y minimum")
    bbox_xmax: Optional[int] = Field(
        None, ge=0, description="Bounding box x maximum")
    bbox_ymax: Optional[int] = Field(
        None, ge=0, description="Bounding box y maximum")


class AnnotationCreate(AnnotationBase):
    """Schema for creating a new annotation"""
    image_id: int = Field(..., gt=0,
                          description="ID of the image this annotation belongs to")
    label_id: int = Field(..., gt=0,
                          description="ID of the label for this annotation")


class AnnotationUpdate(BaseModel):
    """Schema for updating an annotation"""
    bbox_xmin: Optional[int] = Field(None, ge=0)
    bbox_ymin: Optional[int] = Field(None, ge=0)
    bbox_xmax: Optional[int] = Field(None, ge=0)
    bbox_ymax: Optional[int] = Field(None, ge=0)
    label_id: Optional[int] = Field(None, gt=0)


class Annotation(AnnotationBase):
    """Schema for annotation response"""
    id: int = Field(..., description="Annotation ID")
    image_id: int = Field(..., description="Image ID")
    label_id: int = Field(..., description="Label ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True


class AnnotationWithImage(Annotation):
    """Schema for annotation with associated image"""
    image: "Image" = Field(..., description="Image this annotation belongs to")

    class Config:
        from_attributes = True


class AnnotationWithLabel(Annotation):
    """Schema for annotation with associated label"""
    label_obj: "Label" = Field(...,
                               description="Label object for this annotation")

    class Config:
        from_attributes = True


class AnnotationWithImageAndLabel(Annotation):
    """Schema for annotation with both image and label"""
    image: "Image" = Field(..., description="Image this annotation belongs to")
    label_obj: "Label" = Field(...,
                               description="Label object for this annotation")

    class Config:
        from_attributes = True
