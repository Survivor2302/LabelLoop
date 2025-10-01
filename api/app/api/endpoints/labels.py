from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.api.deps import get_label_service
from app.services.label_service import LabelService
from app.schema.label import (
    Label,
    LabelCreate,
    LabelUpdate,
    LabelWithDataset,
    LabelWithAnnotations
)

router = APIRouter(prefix="/labels", tags=["labels"])


@router.post("/", response_model=Label, status_code=status.HTTP_201_CREATED)
def create_label(
    label: LabelCreate,
    service: LabelService = Depends(get_label_service)
):
    """Create a new label"""
    return service.create_label(label)


@router.get("/", response_model=List[Label])
def get_all_labels(
    skip: int = Query(0, ge=0, description="Number of labels to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Number of labels to return"),
    service: LabelService = Depends(get_label_service)
):
    """Get all labels across all datasets"""
    return service.get_all_labels(skip=skip, limit=limit)


@router.get("/dataset/{dataset_id}", response_model=List[Label])
def get_labels_by_dataset(
    dataset_id: int,
    skip: int = Query(0, ge=0, description="Number of labels to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Number of labels to return"),
    service: LabelService = Depends(get_label_service)
):
    """Get all labels for a specific dataset"""
    return service.get_labels_by_dataset(dataset_id, skip=skip, limit=limit)


@router.get("/search", response_model=List[Label])
def search_labels(
    q: str = Query(..., min_length=1, description="Search query"),
    dataset_id: Optional[int] = Query(
        None, description="Filter by dataset ID"),
    service: LabelService = Depends(get_label_service)
):
    """Search labels by name"""
    return service.search_labels(q, dataset_id)


@router.get("/{label_id}", response_model=Label)
def get_label(
    label_id: int,
    service: LabelService = Depends(get_label_service)
):
    """Get a label by ID"""
    label = service.get_label(label_id)

    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )

    return label


@router.get("/{label_id}/with-dataset", response_model=LabelWithDataset)
def get_label_with_dataset(
    label_id: int,
    service: LabelService = Depends(get_label_service)
):
    """Get a label with its associated dataset"""
    label = service.get_label_with_dataset(label_id)

    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )

    return label


@router.get("/{label_id}/with-annotations", response_model=LabelWithAnnotations)
def get_label_with_annotations(
    label_id: int,
    service: LabelService = Depends(get_label_service)
):
    """Get a label with its associated annotations"""
    label = service.get_label_with_annotations(label_id)

    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )

    return label


@router.get("/{label_id}/stats")
def get_label_stats(
    label_id: int,
    service: LabelService = Depends(get_label_service)
):
    """Get statistics for a label"""
    return service.get_label_stats(label_id)


@router.put("/{label_id}", response_model=Label)
def update_label(
    label_id: int,
    label_update: LabelUpdate,
    service: LabelService = Depends(get_label_service)
):
    """Update a label"""
    label = service.update_label(label_id, label_update)

    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )

    return label


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
