from fastapi import APIRouter
from app.api.endpoints.health import router as health_router
# Router principal sans versioning
api_router = APIRouter()
# Include health endpoints
api_router.include_router(health_router)
