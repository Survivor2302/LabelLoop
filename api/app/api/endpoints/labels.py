from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.api.deps import get_label_service
from app.services.label_service import LabelService
from app.schema.label import (
    Label,
    LabelCreate,
    LabelListResponse
)

router = APIRouter(prefix="/labels", tags=["labels"])


@router.post("/", response_model=Label, status_code=status.HTTP_201_CREATED)
def create_label(
    label: LabelCreate,
    service: LabelService = Depends(get_label_service)
):
    """Create a new label"""
    return service.create_label(label)


@router.get("/", response_model=LabelListResponse)
def get_labels(
    skip: int = Query(0, ge=0, description="Number of labels to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Number of labels to return"),
    search: Optional[str] = Query(None, description="Search in label name"),
    service: LabelService = Depends(get_label_service)
):
    """Get all labels with search and total count"""
    return service.get_labels(skip=skip, limit=limit, search=search)


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(
    label_id: int,
    service: LabelService = Depends(get_label_service)
):
    """Delete a label"""
    success = service.delete_label(label_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
