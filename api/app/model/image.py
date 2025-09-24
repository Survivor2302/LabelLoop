from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(500), nullable=False, unique=True, index=True)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    dataset_id = Column(Integer, ForeignKey(
        "datasets.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)

    # Relation vers Dataset (many-to-one)
    dataset = relationship("Dataset", back_populates="images")
    
    # Relation vers Annotation (one-to-many)
    annotations = relationship(
        "Annotation", back_populates="image", cascade="all, delete-orphan")
