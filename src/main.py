import logging
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.config.settings import settings
from src.config.logging import setup_logging

                    
logger = setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API for the AI Task Management Platform",
        version="1.0.0"
    )

                              
    Instrumentator().instrument(app).expose(app)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.PROJECT_NAME}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(f"Shutting down {settings.PROJECT_NAME}")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
