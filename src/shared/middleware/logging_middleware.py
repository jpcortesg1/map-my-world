"""Logging middleware for Map My World API."""
import time
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.shared.logging.logger import get_logger
from src.shared.logging.formatters import format_request_log, format_response_log

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """Process request and log information."""
        start_time = time.time()
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Get user agent
        user_agent = request.headers.get("user-agent")
        
        # Log incoming request
        logger.info(
            format_request_log(
                method=request.method,
                path=request.url.path,
                client_ip=client_ip,
                user_agent=user_agent
            )
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate response time
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Log response
        logger.info(
            format_response_log(
                status_code=response.status_code,
                response_time_ms=response_time
            )
        )
        
        return response 