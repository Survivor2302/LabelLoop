from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, asc, or_
from typing import List, Optional
from app.model.dataset import Dataset
from app.model.label import Label
from app.model.image import Image
from app.schema.dataset import DatasetCreate, DatasetUpdate
from fastapi import HTTPException, status


class DatasetService:
    """Service for managing datasets"""

    def __init__(self, db: Session):
        self.db = db

    def create_dataset(self, dataset_data: DatasetCreate) -> Dataset:
        """Create a new dataset with optional labels"""
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
            description=dataset_data.description
        )

        self.db.add(db_dataset)
        self.db.flush()  # Flush to get the ID without committing yet

        # Handle labels if provided
        if dataset_data.label_names:
            for label_name in dataset_data.label_names:
                # Check if label already exists
                label = self.db.query(Label).filter(
                    Label.name == label_name).first()

                # If label doesn't exist, create it
                if not label:
                    label = Label(name=label_name)
                    self.db.add(label)
                    self.db.flush()

                # Associate label with dataset
                if label not in db_dataset.labels:
                    db_dataset.labels.append(label)

        self.db.commit()
        self.db.refresh(db_dataset)

        return db_dataset

    def get_dataset(self, dataset_id: int) -> Optional[Dataset]:
        """Get a dataset by ID"""
        return self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    def get_dataset_detail(self, dataset_id: int) -> Optional[dict]:
        """Get detailed dataset information with counts"""
        dataset = self.db.query(Dataset).filter(
            Dataset.id == dataset_id).first()
        
        if not dataset:
            return None
        
        # Count images
        image_count = len(dataset.images) if dataset.images else 0

        # Count annotations across all images in the dataset
        from app.model.annotation import Annotation
        annotation_count = self.db.query(Annotation).join(Image).filter(
            Image.dataset_id == dataset_id
        ).count()
        
        # Count labels
        label_count = len(dataset.labels) if dataset.labels else 0
        
        return {
            "id": dataset.id,
            "name": dataset.name,
            "description": dataset.description,
            "created_at": dataset.created_at,
            "updated_at": dataset.updated_at,
            "image_count": image_count,
            "annotation_count": annotation_count,
            "label_count": label_count
        }

    def get_datasets(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        label_name: Optional[str] = None,
        sort_by: str = "name",
        sort_order: str = "asc"
    ) -> List[Dataset]:
        """Get all datasets with search, filtering and sorting"""
        query = self.db.query(Dataset)

        # Add image count for sorting
        query = query.outerjoin(Image).group_by(Dataset.id)

        # Add label filtering if specified
        if label_name:
            query = query.join(Dataset.labels).filter(
                Label.name.ilike(f"%{label_name}%"))

        # Add text search
        if search:
            query = query.filter(
                or_(
                    Dataset.name.ilike(f"%{search}%"),
                    Dataset.description.ilike(f"%{search}%")
                )
            )

        # Add sorting
        if sort_by == "id":
            order_func = asc(
                Dataset.id) if sort_order == "asc" else desc(Dataset.id)
        elif sort_by == "name":
            order_func = asc(
                Dataset.name) if sort_order == "asc" else desc(Dataset.name)
        elif sort_by == "created_at":
            order_func = asc(Dataset.created_at) if sort_order == "asc" else desc(
                Dataset.created_at)
        elif sort_by == "image_count":
            order_func = asc(func.count(Image.id)) if sort_order == "asc" else desc(
                func.count(Image.id))
        else:
            order_func = asc(Dataset.id)  # Default fallback

        query = query.order_by(order_func)

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

    def add_label_to_dataset(self, dataset_id: int, label_id: int) -> bool:
        """Add a label to a dataset"""
        dataset = self.get_dataset(dataset_id)
        label = self.db.query(Label).filter(Label.id == label_id).first()

        if not dataset or not label:
            return False

        if label not in dataset.labels:
            dataset.labels.append(label)
            self.db.commit()

        return True

    def remove_label_from_dataset(self, dataset_id: int, label_id: int) -> bool:
        """Remove a label from a dataset"""
        dataset = self.get_dataset(dataset_id)
        label = self.db.query(Label).filter(Label.id == label_id).first()

        if not dataset or not label:
            return False

        if label in dataset.labels:
            dataset.labels.remove(label)
            self.db.commit()

        return True
