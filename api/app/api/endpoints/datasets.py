from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.api.deps import get_dataset_service
from app.services.dataset_service import DatasetService
from app.schema.dataset import (
    Dataset,
    DatasetCreate,
    DatasetUpdate,
    DatasetWithImages,
    DatasetDetail
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
    search: Optional[str] = Query(
        None, description="Search in dataset name and description"),
    label_name: Optional[str] = Query(
        None, description="Filter by label name"),
    sort_by: str = Query(
        "id", description="Sort by: id, name, created_at, image_count"),
    sort_order: str = Query("desc", description="Sort order: asc, desc"),
    service: DatasetService = Depends(get_dataset_service)
):
    """Get all datasets with search, filtering and sorting"""
    return service.get_datasets(
        skip=skip,
        limit=limit,
        search=search,
        label_name=label_name,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/{dataset_id}", response_model=DatasetDetail)
def get_dataset(
    dataset_id: int,
    service: DatasetService = Depends(get_dataset_service)
):
    """Get detailed dataset information with counts"""
    dataset = service.get_dataset_detail(dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    return dataset


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
