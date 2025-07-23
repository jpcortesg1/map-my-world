"""FastAPI application factory for Map My World API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.core import get_settings
from src.shared.middleware.error_handler import ErrorHandlerMiddleware
from src.shared.middleware.logging_middleware import LoggingMiddleware
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Factory to create the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Map My World API",
        description="API for exploring and reviewing locations",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Middleware
    app.add_middleware(CORSMiddleware, **settings.cors_settings)
    app.add_middleware(ErrorHandlerMiddleware)
    app.add_middleware(LoggingMiddleware)
    
    # Register routes
    from src.lib.locations.infrastructure.api.routes import router as locations_router
    from src.lib.categories.infrastructure.api.routes import router as categories_router
    from src.lib.recommendations.infrastructure.api.routes import router as recommendations_router
    
    app.include_router(locations_router, prefix="/api/v1")
    app.include_router(categories_router, prefix="/api/v1")
    app.include_router(recommendations_router, prefix="/api/v1")
    
    logger.info("FastAPI application initialized successfully")
    return app 