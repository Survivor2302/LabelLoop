from fastapi import APIRouter, Depends
from app.api.deps import get_health_service
from app.services.health_service import HealthService
from app.schema.health import Health, DBHealth


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=Health)
def health(health_service: HealthService = Depends(get_health_service)):
    return health_service.check_app()
