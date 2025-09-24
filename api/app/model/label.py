from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    dataset_id = Column(Integer, ForeignKey(
        "datasets.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    # Relation vers Dataset (many-to-one)
    dataset = relationship("Dataset", back_populates="labels")

    # Relation vers Annotation (one-to-many)
    annotations = relationship(
        "Annotation", back_populates="label_obj", cascade="all, delete-orphan")
