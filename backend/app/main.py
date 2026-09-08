from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import notes
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import setup_logging, logger


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


def create_application() -> FastAPI:
    # 1. Anzisha Logging kabla ya kila kitu
    setup_logging()
    logger.info("Starting up Notes Application...")

    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS Standard Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API Routers
    application.include_router(notes.router, prefix=settings.API_V1_STR)

    @application.get("/health", tags=["Health Check"])
    async def health_check():
        logger.info("Health check endpoint accessed.")
        return {"status": "healthy", "version": settings.VERSION}

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)