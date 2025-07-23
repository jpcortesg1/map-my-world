"""Base exception class for Map My World API."""
from typing import List, Dict, Optional


class MapMyWorldException(Exception):
    """Base exception for Map My World API."""
    
    def __init__(
        self, 
        status_code: int, 
        error: str, 
        details: Optional[List[Dict[str, str]]] = None
    ) -> None:
        self.status_code = status_code
        self.error = error
        self.details = details or []
        super().__init__(error) 