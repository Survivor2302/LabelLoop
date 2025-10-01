from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.api.deps import get_dataset_service
from app.services.dataset_service import DatasetService
from app.schema.dataset import (
    Dataset,
    DatasetCreate,
    DatasetUpdate,
    DatasetStatus,
    DatasetWithImages
)

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/", response_model=Dataset, status_code=status.HTTP_201_CREATED)
def create_dataset(
    dataset: DatasetCreate,
    service: DatasetService = Depends(get_dataset_service)
):
    """Create a new dataset"""
    return service.create_dataset(dataset)


@router.get("/", response_model=List[Dataset])
def get_datasets(
    skip: int = Query(0, ge=0, description="Number of datasets to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Number of datasets to return"),
    status_filter: Optional[DatasetStatus] = Query(
        None, description="Filter by dataset status"),
    service: DatasetService = Depends(get_dataset_service)
):
    """Get all datasets with optional filtering"""
    return service.get_datasets(skip=skip, limit=limit, status_filter=status_filter)


@router.get("/{dataset_id}", response_model=Dataset)
def get_dataset(
    dataset_id: int,
    service: DatasetService = Depends(get_dataset_service)
):
    """Get a dataset by ID"""
    dataset = service.get_dataset(dataset_id)

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    return dataset


@router.get("/{dataset_id}/with-images", response_model=DatasetWithImages)
def get_dataset_with_images(
    dataset_id: int,
    service: DatasetService = Depends(get_dataset_service)
):
    """Get a dataset with its associated images"""
    dataset = service.get_dataset_with_images(dataset_id)

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    return dataset


@router.get("/{dataset_id}/stats")
def get_dataset_stats(
    dataset_id: int,
    service: DatasetService = Depends(get_dataset_service)
):
    """Get statistics for a dataset"""
    return service.get_dataset_stats(dataset_id)


@router.put("/{dataset_id}", response_model=Dataset)
def update_dataset(
    dataset_id: int,
    dataset_update: DatasetUpdate,
    service: DatasetService = Depends(get_dataset_service)
):
    """Update a dataset"""
    dataset = service.update_dataset(dataset_id, dataset_update)

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    return dataset


@router.patch("/{dataset_id}/status", response_model=Dataset)
def change_dataset_status(
    dataset_id: int,
    new_status: DatasetStatus,
    service: DatasetService = Depends(get_dataset_service)
):
    """Change the status of a dataset"""
    dataset = service.change_dataset_status(dataset_id, new_status)

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    return dataset


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dataset(
    dataset_id: int,
    service: DatasetService = Depends(get_dataset_service)
):
    """Delete a dataset"""
    success = service.delete_dataset(dataset_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
