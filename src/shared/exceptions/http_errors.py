"""HTTP error exceptions for Map My World API."""
from typing import List, Dict, Optional
from .base import MapMyWorldException


class BadRequestError(MapMyWorldException):
    """400 Bad Request error."""
    
    def __init__(self, error: str = "Bad Request", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=400, error=error, details=details)


class UnauthorizedError(MapMyWorldException):
    """401 Unauthorized error."""
    
    def __init__(self, error: str = "Unauthorized", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=401, error=error, details=details)


class ForbiddenError(MapMyWorldException):
    """403 Forbidden error."""
    
    def __init__(self, error: str = "Forbidden", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=403, error=error, details=details)


class NotFoundError(MapMyWorldException):
    """404 Not Found error."""
    
    def __init__(self, error: str = "Not Found", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=404, error=error, details=details)


class ConflictError(MapMyWorldException):
    """409 Conflict error."""
    
    def __init__(self, error: str = "Conflict", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=409, error=error, details=details)


class UnprocessableEntityError(MapMyWorldException):
    """422 Unprocessable Entity error."""
    
    def __init__(self, error: str = "Unprocessable Entity", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=422, error=error, details=details)


class InternalServerError(MapMyWorldException):
    """500 Internal Server Error."""
    
    def __init__(self, error: str = "Internal Server Error", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=500, error=error, details=details)


class BadGatewayError(MapMyWorldException):
    """502 Bad Gateway error."""
    
    def __init__(self, error: str = "Bad Gateway", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=502, error=error, details=details)


class ServiceUnavailableError(MapMyWorldException):
    """503 Service Unavailable error."""
    
    def __init__(self, error: str = "Service Unavailable", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=503, error=error, details=details)


class GatewayTimeoutError(MapMyWorldException):
    """504 Gateway Timeout error."""
    
    def __init__(self, error: str = "Gateway Timeout", details: Optional[List[Dict[str, str]]] = None) -> None:
        super().__init__(status_code=504, error=error, details=details) 