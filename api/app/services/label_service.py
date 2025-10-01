from sqlalchemy.orm import Session
from typing import List, Optional
from app.model.label import Label
from app.model.dataset import Dataset
from app.schema.label import LabelCreate, LabelUpdate
from fastapi import HTTPException, status


class LabelService:
    """Service for managing labels"""

    def __init__(self, db: Session):
        self.db = db

    def create_label(self, label_data: LabelCreate) -> Label:
        """Create a new label"""
        # Check if dataset exists
        dataset = self.db.query(Dataset).filter(
            Dataset.id == label_data.dataset_id
        ).first()

        if not dataset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset with ID {label_data.dataset_id} not found"
            )

        # Check if label with same name already exists in this dataset
        existing_label = self.db.query(Label).filter(
            Label.name == label_data.name,
            Label.dataset_id == label_data.dataset_id
        ).first()

        if existing_label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Label with name '{label_data.name}' already exists in this dataset"
            )

        # Create new label
        db_label = Label(
            name=label_data.name,
            dataset_id=label_data.dataset_id
        )

        self.db.add(db_label)
        self.db.commit()
        self.db.refresh(db_label)

        return db_label

    def get_label(self, label_id: int) -> Optional[Label]:
        """Get a label by ID"""
        return self.db.query(Label).filter(Label.id == label_id).first()

    def get_labels_by_dataset(
        self,
        dataset_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Label]:
        """Get all labels for a specific dataset"""
        # Check if dataset exists
        dataset = self.db.query(Dataset).filter(
            Dataset.id == dataset_id).first()

        if not dataset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset with ID {dataset_id} not found"
            )

        return self.db.query(Label).filter(
            Label.dataset_id == dataset_id
        ).offset(skip).limit(limit).all()

    def get_all_labels(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Label]:
        """Get all labels across all datasets"""
        return self.db.query(Label).offset(skip).limit(limit).all()

    def update_label(self, label_id: int, label_data: LabelUpdate) -> Optional[Label]:
        """Update a label"""
        db_label = self.get_label(label_id)

        if not db_label:
            return None

        # Check if new name conflicts with existing label in the same dataset
        if label_data.name and label_data.name != db_label.name:
            existing_label = self.db.query(Label).filter(
                Label.name == label_data.name,
                Label.dataset_id == db_label.dataset_id,
                Label.id != label_id
            ).first()

            if existing_label:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Label with name '{label_data.name}' already exists in this dataset"
                )

        # Update fields
        update_data = label_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_label, field, value)

        self.db.commit()
        self.db.refresh(db_label)

        return db_label

    def delete_label(self, label_id: int) -> bool:
        """Delete a label"""
        db_label = self.get_label(label_id)

        if not db_label:
            return False

        self.db.delete(db_label)
        self.db.commit()

        return True

    def get_label_with_dataset(self, label_id: int) -> Optional[Label]:
        """Get a label with its associated dataset"""
        return self.db.query(Label).filter(
            Label.id == label_id
        ).first()

    def get_label_with_annotations(self, label_id: int) -> Optional[Label]:
        """Get a label with its associated annotations"""
        return self.db.query(Label).filter(
            Label.id == label_id
        ).first()

    def get_label_stats(self, label_id: int) -> dict:
        """Get statistics for a label"""
        db_label = self.get_label(label_id)

        if not db_label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found"
            )

        # Count annotations
        annotation_count = len(
            db_label.annotations) if db_label.annotations else 0

        return {
            "label_id": label_id,
            "name": db_label.name,
            "dataset_id": db_label.dataset_id,
            "dataset_name": db_label.dataset.name if db_label.dataset else None,
            "annotation_count": annotation_count,
            "created_at": db_label.created_at,
            "updated_at": db_label.updated_at
        }

    def search_labels(self, query: str, dataset_id: Optional[int] = None) -> List[Label]:
        """Search labels by name"""
        search_query = self.db.query(Label).filter(
            Label.name.ilike(f"%{query}%")
        )

        if dataset_id:
            search_query = search_query.filter(Label.dataset_id == dataset_id)

        return search_query.all()
