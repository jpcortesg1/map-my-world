"""Error handling middleware for Map My World API."""
import time
from typing import Any
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.shared.exceptions.base import MapMyWorldException
from src.shared.logging.logger import get_logger
from src.shared.logging.formatters import format_error_log

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions and convert them to HTTP responses."""
    
    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """Process request and handle any exceptions."""
        start_time = time.time()
        
        try:
            response = await call_next(request)
            return response
            
        except MapMyWorldException as e:
            # Handle application-specific exceptions
            logger.error(
                format_error_log(
                    e, 
                    {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": e.status_code
                    }
                )
            )
            
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "status_code": e.status_code,
                    "error": e.error,
                    "details": e.details,
                }
            )
            
        except Exception as e:
            # Handle unexpected exceptions
            logger.error(
                format_error_log(
                    e,
                    {
                        "method": request.method,
                        "path": request.url.path,
                        "exception_type": type(e).__name__
                    }
                )
            )
            
            return JSONResponse(
                status_code=500,
                content={
                    "status_code": 500,
                    "error": "Internal Server Error",
                    "details": [
                        {
                            "field": "server",
                            "message": "An unexpected error occurred"
                        }
                    ],
                }
            ) 