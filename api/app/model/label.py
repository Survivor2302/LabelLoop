from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)

    # Relation vers Dataset (many-to-many via dataset_labels)
    datasets = relationship(
        "Dataset", secondary="dataset_labels", back_populates="labels")

    # Relation vers Annotation (one-to-many)
    annotations = relationship(
        "Annotation", back_populates="label_obj", cascade="all, delete-orphan")
