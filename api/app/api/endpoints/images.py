from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db, get_image_service
from app.services.image_service import ImageService
from app.model.image import ImageStatus
from app.schema.image import (
    Image,
    ImageUpdate,
    ImageUploadBatchRequest,
    ImageUploadBatchResponse,
    ImageUploadResponse,
    ImageConfirmUploadRequest,
    ImageWithDownloadUrl,
    ImageListResponse,
    ImageWithUrlListResponse
)

router = APIRouter()


@router.post("/datasets/{dataset_id}/images/prepare-upload", response_model=ImageUploadBatchResponse)
def prepare_upload(
    dataset_id: int = Path(..., gt=0, description="Dataset ID"),
    request: ImageUploadBatchRequest = ...,
    service: ImageService = Depends(get_image_service)
):
    """
    Prepare batch upload: create image records and generate presigned URLs

    This endpoint:
    1. Creates image records in DB with 'uploading' status
    2. Generates presigned URLs for direct upload to S3
    3. Returns upload URLs that expire in 1 hour
    """
    uploads = service.prepare_upload(dataset_id, request.files)

    if not uploads:
        raise HTTPException(
            status_code=500, detail="Failed to prepare uploads")

    return ImageUploadBatchResponse(uploads=uploads)


@router.post("/datasets/{dataset_id}/images/confirm-upload")
def confirm_upload(
    dataset_id: int = Path(..., gt=0, description="Dataset ID"),
    request: ImageConfirmUploadRequest = ...,
    service: ImageService = Depends(get_image_service)
):
    """
    Confirm successful uploads

    Updates image status from 'uploading' to 'uploaded' after verifying
    that files exist in S3.
    """
    updated_count = service.confirm_upload(request.image_ids)

    return {
        "message": f"Successfully confirmed {updated_count} uploads",
        "updated_count": updated_count,
        "total_requested": len(request.image_ids)
    }


@router.get("/datasets/{dataset_id}/images", response_model=ImageListResponse)
def get_dataset_images(
    dataset_id: int = Path(..., gt=0, description="Dataset ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Max number of records to return"),
    status: Optional[ImageStatus] = Query(
        None, description="Filter by status"),
    service: ImageService = Depends(get_image_service)
):
    """
    Get all images for a specific dataset (without download URLs)

    Returns paginated list with total count for pagination.
    """
    return service.get_images(skip=skip, limit=limit, dataset_id=dataset_id, status=status)


@router.get("/datasets/{dataset_id}/images/with-urls", response_model=ImageWithUrlListResponse)
def get_dataset_images_with_urls(
    dataset_id: int = Path(..., gt=0, description="Dataset ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000,
                       description="Max number of records to return"),
    status: Optional[ImageStatus] = Query(
        None, description="Filter by status"),
    expires_in: int = Query(3600, ge=60, le=604800,
                            description="URL expiration in seconds (default: 1h, max: 7 days)"),
    service: ImageService = Depends(get_image_service)
):
    """
    Get all images for a specific dataset WITH presigned download URLs

    Returns paginated list with total count for pagination.
    This endpoint generates presigned URLs for all images in one go,
    avoiding N+1 requests. URLs are only generated for images with status 'uploaded'.
    """
    return service.get_images_with_download_urls(
        skip=skip,
        limit=limit,
        dataset_id=dataset_id,
        status=status,
        expires_in=expires_in
    )


@router.get("/images/{image_id}", response_model=Image)
def get_image(
    image_id: int = Path(..., gt=0, description="Image ID"),
    service: ImageService = Depends(get_image_service)
):
    """Get a single image by ID"""
    db_image = service.get_image(image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.get("/images/{image_id}/download-url")
def get_download_url(
    image_id: int = Path(..., gt=0, description="Image ID"),
    expires_in: int = Query(3600, ge=60, le=604800,
                            description="URL expiration in seconds"),
    service: ImageService = Depends(get_image_service)
):
    """
    Generate a presigned URL for downloading an image

    URL expires after the specified time (default: 1 hour, max: 7 days)
    """
    download_url = service.generate_download_url(image_id, expires_in)

    if not download_url:
        raise HTTPException(
            status_code=404,
            detail="Image not found or not yet uploaded"
        )

    return {
        "download_url": download_url,
        "expires_in": expires_in
    }


@router.patch("/images/{image_id}", response_model=Image)
def update_image(
    image_id: int = Path(..., gt=0, description="Image ID"),
    image_data: ImageUpdate = ...,
    service: ImageService = Depends(get_image_service)
):
    """Update an image (mainly for dimensions or status)"""
    db_image = service.update_image(image_id, image_data)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.delete("/images/{image_id}")
def delete_image(
    image_id: int = Path(..., gt=0, description="Image ID"),
    service: ImageService = Depends(get_image_service)
):
    """Delete an image (removes from both DB and S3)"""
    success = service.delete_image(image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}


@router.delete("/datasets/{dataset_id}/images")
def delete_all_dataset_images(
    dataset_id: int = Path(..., gt=0, description="Dataset ID"),
    service: ImageService = Depends(get_image_service)
):
    """
    Delete ALL images for a specific dataset
    
    ⚠️ WARNING: This will permanently delete all images from both DB and S3.
    This operation cannot be undone!

    Returns statistics about the deletion operation.
    """
    result = service.delete_all_dataset_images(dataset_id)
    return result
