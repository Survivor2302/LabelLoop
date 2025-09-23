from time import perf_counter
from sqlalchemy import text
from sqlalchemy.engine import Engine
from app.core.config import settings
from app.core.s3 import s3_client
from app.schema.health import Health, DBHealth, ComponentHealth, S3Health


class HealthService:
    def __init__(self, engine: Engine):
        self.engine = engine

    def check_app(self) -> Health:
        api_component = ComponentHealth(status="ok")
        db_component = self.check_db()
        s3_component = self.check_s3()

        components = {
            "api": api_component,
            "db": db_component,
            "s3": s3_component,
        }

        has_error = any(c.status == "error" for c in components.values())
        global_status = "degraded" if has_error else "ok"

        return Health(status=global_status, components=components)

    def check_db(self) -> DBHealth:
        if not settings.database_url:
            return DBHealth(status="error", message="DATABASE_URL is not configured")

        try:
            start = perf_counter()
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                value = result.scalar()
                latency_ms = (perf_counter() - start) * 1000.0
                if value == 1:
                    return DBHealth(status="ok", latency_ms=latency_ms)
                return DBHealth(status="error", message="Unexpected DB response", latency_ms=latency_ms)
        except Exception as exc:  # noqa: BLE001
            if settings.DEBUG:
                return DBHealth(status="error", message=str(exc))
            return DBHealth(status="error")

    def check_s3(self) -> S3Health:
        if not s3_client.is_configured():
            return S3Health(status="error", message="S3 configuration is incomplete")
        
        try:
            success, message, latency_ms = s3_client.test_connection()
            if success:
                return S3Health(status="ok", latency_ms=latency_ms)
            else:
                return S3Health(status="error", message=message, latency_ms=latency_ms)
        except Exception as exc:  # noqa: BLE001
            if settings.DEBUG:
                return S3Health(status="error", message=str(exc))
            return S3Health(status="error", message="S3 connection failed")
