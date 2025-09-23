from pydantic import BaseModel
from typing import Optional, Dict, Literal


class ComponentHealth(BaseModel):
    status: Literal["ok", "error"]
    message: Optional[str] = None
    latency_ms: Optional[float] = None


class Health(BaseModel):
    status: Literal["ok", "degraded"]
    components: Dict[str, ComponentHealth]


class DBHealth(ComponentHealth):
    pass


class S3Health(ComponentHealth):
    pass
