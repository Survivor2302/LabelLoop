from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"),
                      nullable=False, index=True)
    label_id = Column(Integer, ForeignKey("labels.id"),
                      nullable=False, index=True)
    bbox_xmin = Column(Integer, nullable=True,
                       comment="Bounding box x minimum")
    bbox_ymin = Column(Integer, nullable=True,
                       comment="Bounding box y minimum")
    bbox_xmax = Column(Integer, nullable=True,
                       comment="Bounding box x maximum")
    bbox_ymax = Column(Integer, nullable=True,
                       comment="Bounding box y maximum")
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)

    # Relation vers Image (many-to-one)
    image = relationship("Image", back_populates="annotations")

    # Relation vers Label (many-to-one)
    label_obj = relationship("Label", back_populates="annotations")
