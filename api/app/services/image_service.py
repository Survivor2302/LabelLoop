from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from app.model.image import Image, ImageStatus
from app.schema.image import ImageCreate, ImageUpdate, ImageUploadRequest
from app.core.s3 import s3_client


class ImageService:
    """Service for image business logic"""

    def __init__(self, db: Session):
        self.db = db

    def generate_s3_key(self, dataset_id: int, filename: str) -> str:
        """
        Generate a unique S3 key for an image
        Format: datasets/{dataset_id}/images/{uuid}_{filename}
        """
        unique_id = str(uuid.uuid4())
        # Sanitize filename to avoid issues
        safe_filename = filename.replace(" ", "_")
        return f"datasets/{dataset_id}/images/{unique_id}_{safe_filename}"

    def create_image_record(
        self,
        dataset_id: int,
        file_info: ImageUploadRequest,
        s3_key: str
    ) -> Image:
        """
        Create an image record in DB with 'uploading' status
        """
        db_image = Image(
            filename=file_info.filename,
            s3_key=s3_key,
            file_size=file_info.file_size,
            mime_type=file_info.mime_type,
            status=ImageStatus.UPLOADING,
            dataset_id=dataset_id
        )
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)
        return db_image

    def prepare_upload(
        self,
        dataset_id: int,
        files: List[ImageUploadRequest]
    ) -> List[dict]:
        """
        Prepare batch upload: create DB records and generate presigned URLs

        Returns list of dicts with:
        - image_id
        - upload_url
        - s3_key
        - expires_in
        """
        uploads = []

        for file_info in files:
            # Generate unique S3 key
            s3_key = self.generate_s3_key(dataset_id, file_info.filename)

            # Create DB record with 'uploading' status
            db_image = self.create_image_record(dataset_id, file_info, s3_key)

            # Generate presigned URL
            upload_url = s3_client.generate_presigned_upload_url(
                s3_key=s3_key,
                content_type=file_info.mime_type,
                expires_in=3600  # 1 hour
            )

            if not upload_url:
                # If URL generation fails, mark image as error
                db_image.status = ImageStatus.ERROR
                self.db.commit()
                continue

            uploads.append({
                "image_id": db_image.id,
                "upload_url": upload_url,
                "s3_key": s3_key,
                "expires_in": 3600
            })

        return uploads

    def confirm_upload(self, image_ids: List[int]) -> int:
        """
        Confirm successful uploads by updating status to 'uploaded'
        Returns number of images updated
        """
        count = 0
        for image_id in image_ids:
            db_image = self.db.query(Image).filter(
                Image.id == image_id).first()
            if db_image and db_image.status == ImageStatus.UPLOADING:
                # Verify file exists in S3
                if s3_client.file_exists(db_image.s3_key):
                    db_image.status = ImageStatus.UPLOADED
                    count += 1
                else:
                    db_image.status = ImageStatus.ERROR

        self.db.commit()
        return count

    def mark_as_error(self, image_id: int) -> bool:
        """Mark an image as error"""
        db_image = self.db.query(Image).filter(Image.id == image_id).first()
        if db_image:
            db_image.status = ImageStatus.ERROR
            self.db.commit()
            return True
        return False

    def get_images(
        self,
        skip: int = 0,
        limit: int = 100,
        dataset_id: Optional[int] = None,
        status: Optional[ImageStatus] = None
    ) -> dict:
        """Get images with optional filters and total count"""
        query = self.db.query(Image)

        if dataset_id:
            query = query.filter(Image.dataset_id == dataset_id)
        if status:
            query = query.filter(Image.status == status)

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return {"total": total, "items": items}

    def get_image(self, image_id: int) -> Optional[Image]:
        """Get a single image by ID"""
        return self.db.query(Image).filter(Image.id == image_id).first()

    def update_image(self, image_id: int, image_data: ImageUpdate) -> Optional[Image]:
        """Update an image"""
        db_image = self.get_image(image_id)
        if not db_image:
            return None

        update_data = image_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_image, field, value)

        self.db.commit()
        self.db.refresh(db_image)
        return db_image

    def delete_image(self, image_id: int) -> bool:
        """Delete an image (from DB and S3)"""
        db_image = self.get_image(image_id)
        if not db_image:
            return False

        # Delete from S3
        s3_client.delete_file(db_image.s3_key)

        # Delete from DB
        self.db.delete(db_image)
        self.db.commit()
        return True

    def delete_all_dataset_images(self, dataset_id: int) -> dict:
        """
        Delete all images for a specific dataset (from DB and S3)

        Returns dict with deletion statistics
        """
        # Get all images for this dataset
        images = self.db.query(Image).filter(
            Image.dataset_id == dataset_id).all()

        if not images:
            return {
                "deleted_count": 0,
                "s3_deleted": 0,
                "s3_errors": 0,
                "message": "No images found for this dataset"
            }

        deleted_count = 0
        s3_deleted = 0
        s3_errors = 0

        for image in images:
            # Try to delete from S3
            if s3_client.delete_file(image.s3_key):
                s3_deleted += 1
            else:
                s3_errors += 1

            # Delete from DB
            self.db.delete(image)
            deleted_count += 1

        self.db.commit()

        return {
            "deleted_count": deleted_count,
            "s3_deleted": s3_deleted,
            "s3_errors": s3_errors,
            "message": f"Successfully deleted {deleted_count} images"
        }

    def generate_download_url(self, image_id: int, expires_in: int = 3600) -> Optional[str]:
        """Generate presigned URL for downloading an image"""
        db_image = self.get_image(image_id)
        if not db_image or db_image.status != ImageStatus.UPLOADED:
            return None

        return s3_client.generate_presigned_download_url(
            s3_key=db_image.s3_key,
            expires_in=expires_in
        )

    def get_images_with_download_urls(
        self,
        skip: int = 0,
        limit: int = 100,
        dataset_id: Optional[int] = None,
        status: Optional[ImageStatus] = None,
        expires_in: int = 3600
    ) -> dict:
        """
        Get images with presigned download URLs and total count

        Returns dict with total count and list of images with download URLs
        Only generates URLs for images with status 'uploaded'
        """
        images_data = self.get_images(
            skip=skip, limit=limit, dataset_id=dataset_id, status=status)

        total = images_data["total"]
        images = images_data["items"]

        result = []
        for image in images:
            image_dict = {
                "id": image.id,
                "filename": image.filename,
                "s3_key": image.s3_key,
                "file_size": image.file_size,
                "mime_type": image.mime_type,
                "width": image.width,
                "height": image.height,
                "status": image.status,
                "dataset_id": image.dataset_id,
                "created_at": image.created_at,
                "updated_at": image.updated_at,
                "download_url": None,
                "url_expires_in": None
            }

            # Only generate URL for uploaded images
            if image.status == ImageStatus.UPLOADED:
                download_url = s3_client.generate_presigned_download_url(
                    s3_key=image.s3_key,
                    expires_in=expires_in
                )
                if download_url:
                    image_dict["download_url"] = download_url
                    image_dict["url_expires_in"] = expires_in

            result.append(image_dict)

        return {"total": total, "items": result}
