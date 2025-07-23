#!/usr/bin/env python3
"""Script to run the Map My World API with uvicorn."""
import sys
import os
import uvicorn
from typing import Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.core import get_settings
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


def run_server(
    host: Optional[str] = None,
    port: Optional[int] = None,
    reload: Optional[bool] = None
) -> None:
    """Run uvicorn server with configuration."""
    settings = get_settings()
    
    server_config = {
        "app": "src.main:app",
        "host": host or settings.host,
        "port": port or settings.port,
        "reload": reload if reload is not None else settings.debug,
        "log_level": "info" if not settings.debug else "debug",
        "access_log": True,
    }
    
    logger.info(f"Starting server on http://{server_config['host']}:{server_config['port']}")
    logger.info(f"Debug mode: {server_config['reload']}")
    logger.info("Documentation available at /docs")
    
    uvicorn.run(**server_config)


if __name__ == "__main__":
    run_server() 