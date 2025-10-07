from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


# Table de liaison many-to-many entre datasets et labels
dataset_labels = Table(
    'dataset_labels',
    Base.metadata,
    Column('dataset_id', Integer, ForeignKey('datasets.id'), primary_key=True),
    Column('label_id', Integer, ForeignKey('labels.id'), primary_key=True)
)


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    # Relation vers Image (one-to-many)
    images = relationship("Image", back_populates="dataset",
                          cascade="all, delete-orphan")

    # Relation vers Label (many-to-many via dataset_labels)
    labels = relationship("Label", secondary=dataset_labels,
                          back_populates="datasets")
