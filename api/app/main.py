from fastapi import FastAPI
from app.core.config import settings
from app.api.router import api_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


@app.get("/")
def hello_world():
    return {"message": f"{settings.APP_NAME} - Welcome!"}


# Inclure les routes de l'API
app.include_router(api_router, prefix="/api")
