from fastapi import APIRouter
from app.api.endpoints.health import router as health_router
from app.api.endpoints.datasets import router as datasets_router
from app.api.endpoints.labels import router as labels_router

# Router principal sans versioning
api_router = APIRouter()

# Include health endpoints
api_router.include_router(health_router)

# Include dataset endpoints
api_router.include_router(datasets_router)

# Include label endpoints
api_router.include_router(labels_router)
