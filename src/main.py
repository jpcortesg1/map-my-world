"""Main entry point for Map My World API."""
from src.app import create_app

# Create application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    from config.core import get_settings
    
    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    ) 