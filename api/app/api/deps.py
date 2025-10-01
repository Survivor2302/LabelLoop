from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.services.health_service import HealthService
from app.services.dataset_service import DatasetService
from app.services.label_service import LabelService


def get_health_service() -> HealthService:
    return HealthService(engine)


def get_dataset_service(db: Session = Depends(get_db)) -> DatasetService:
    return DatasetService(db)


def get_label_service(db: Session = Depends(get_db)) -> LabelService:
    return LabelService(db)
