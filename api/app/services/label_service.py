from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.model.label import Label
from app.schema.label import LabelCreate
from fastapi import HTTPException, status


class LabelService:
    """Service for managing labels"""

    def __init__(self, db: Session):
        self.db = db

    def create_label(self, label_data: LabelCreate) -> Label:
        """Create a new label"""
        # Check if label with same name already exists
        existing_label = self.db.query(Label).filter(
            Label.name == label_data.name
        ).first()

        if existing_label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Label with name '{label_data.name}' already exists"
            )

        # Create new label
        db_label = Label(name=label_data.name)

        self.db.add(db_label)
        self.db.commit()
        self.db.refresh(db_label)

        return db_label

    def get_labels(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> dict:
        """Get all labels with optional search and total count"""
        query = self.db.query(Label)

        # Add text search
        if search:
            query = query.filter(Label.name.ilike(f"%{search}%"))

        # Get total count before pagination
        total = query.count()

        # Get paginated results
        items = query.offset(skip).limit(limit).all()

        return {"total": total, "items": items}

    def delete_label(self, label_id: int) -> bool:
        """Delete a label"""
        db_label = self.db.query(Label).filter(Label.id == label_id).first()

        if not db_label:
            return False

        self.db.delete(db_label)
        self.db.commit()

        return True
