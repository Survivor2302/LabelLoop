from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.model.dataset import Dataset
from app.schema.dataset import DatasetCreate, DatasetUpdate, DatasetStatus
from fastapi import HTTPException, status


class DatasetService:
    """Service for managing datasets"""

    def __init__(self, db: Session):
        self.db = db

    def create_dataset(self, dataset_data: DatasetCreate) -> Dataset:
        """Create a new dataset"""
        # Check if dataset with same name already exists
        existing_dataset = self.db.query(Dataset).filter(
            Dataset.name == dataset_data.name
        ).first()

        if existing_dataset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dataset with name '{dataset_data.name}' already exists"
            )

        # Create new dataset
        db_dataset = Dataset(
            name=dataset_data.name,
            description=dataset_data.description,
            status=dataset_data.status
        )

        self.db.add(db_dataset)
        self.db.commit()
        self.db.refresh(db_dataset)

        return db_dataset

    def get_dataset(self, dataset_id: int) -> Optional[Dataset]:
        """Get a dataset by ID"""
        return self.db.query(Dataset).filter(Dataset.id == dataset_id).first()

    def get_datasets(
        self,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[DatasetStatus] = None
    ) -> List[Dataset]:
        """Get all datasets with optional filtering"""
        query = self.db.query(Dataset)

        if status_filter:
            query = query.filter(Dataset.status == status_filter)

        return query.offset(skip).limit(limit).all()

    def update_dataset(self, dataset_id: int, dataset_data: DatasetUpdate) -> Optional[Dataset]:
        """Update a dataset"""
        db_dataset = self.get_dataset(dataset_id)

        if not db_dataset:
            return None

        # Check if new name conflicts with existing dataset
        if dataset_data.name and dataset_data.name != db_dataset.name:
            existing_dataset = self.db.query(Dataset).filter(
                Dataset.name == dataset_data.name,
                Dataset.id != dataset_id
            ).first()

            if existing_dataset:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Dataset with name '{dataset_data.name}' already exists"
                )

        # Update fields
        update_data = dataset_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_dataset, field, value)

        self.db.commit()
        self.db.refresh(db_dataset)

        return db_dataset

    def delete_dataset(self, dataset_id: int) -> bool:
        """Delete a dataset"""
        db_dataset = self.get_dataset(dataset_id)

        if not db_dataset:
            return False

        self.db.delete(db_dataset)
        self.db.commit()

        return True

    def get_dataset_with_images(self, dataset_id: int) -> Optional[Dataset]:
        """Get a dataset with its associated images"""
        return self.db.query(Dataset).filter(
            Dataset.id == dataset_id
        ).first()

    def get_dataset_stats(self, dataset_id: int) -> dict:
        """Get statistics for a dataset"""
        db_dataset = self.get_dataset(dataset_id)

        if not db_dataset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found"
            )

        # Count images and labels
        image_count = len(db_dataset.images) if db_dataset.images else 0
        label_count = len(db_dataset.labels) if db_dataset.labels else 0

        return {
            "dataset_id": dataset_id,
            "name": db_dataset.name,
            "status": db_dataset.status,
            "image_count": image_count,
            "label_count": label_count,
            "created_at": db_dataset.created_at,
            "updated_at": db_dataset.updated_at
        }

    def change_dataset_status(self, dataset_id: int, new_status: DatasetStatus) -> Optional[Dataset]:
        """Change the status of a dataset"""
        db_dataset = self.get_dataset(dataset_id)

        if not db_dataset:
            return None

        db_dataset.status = new_status
        self.db.commit()
        self.db.refresh(db_dataset)

        return db_dataset
