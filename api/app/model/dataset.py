from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from app.schema.dataset import DatasetStatus


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(DatasetStatus), nullable=False,
                    default=DatasetStatus.CREATING)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    # Relation vers Image (one-to-many)
    images = relationship("Image", back_populates="dataset",
                          cascade="all, delete-orphan")
    
    # Relation vers Label (one-to-many)
    labels = relationship("Label", back_populates="dataset",
                          cascade="all, delete-orphan")
