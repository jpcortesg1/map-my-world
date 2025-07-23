"""Domain-specific exceptions for Map My World API."""
from typing import List, Dict, Optional
from .base import MapMyWorldException


class LocationNotFoundError(MapMyWorldException):
    """Location not found error."""
    
    def __init__(self, location_id: int, details: Optional[List[Dict[str, str]]] = None) -> None:
        error = f"Location with ID {location_id} not found"
        if details is None:
            details = [{"field": "location_id", "message": f"Location with ID {location_id} does not exist"}]
        super().__init__(status_code=404, error=error, details=details)


class CategoryNotFoundError(MapMyWorldException):
    """Category not found error."""
    
    def __init__(self, category_id: int, details: Optional[List[Dict[str, str]]] = None) -> None:
        error = f"Category with ID {category_id} not found"
        if details is None:
            details = [{"field": "category_id", "message": f"Category with ID {category_id} does not exist"}]
        super().__init__(status_code=404, error=error, details=details)


class InvalidCoordinatesError(MapMyWorldException):
    """Invalid coordinates error."""
    
    def __init__(self, longitude: float, latitude: float, details: Optional[List[Dict[str, str]]] = None) -> None:
        error = f"Invalid coordinates: longitude={longitude}, latitude={latitude}"
        if details is None:
            details = [
                {"field": "longitude", "message": "Longitude must be between -180 and 180"},
                {"field": "latitude", "message": "Latitude must be between -90 and 90"}
            ]
        super().__init__(status_code=422, error=error, details=details)


class DuplicateLocationError(MapMyWorldException):
    """Duplicate location error."""
    
    def __init__(self, name: str, longitude: float, latitude: float, details: Optional[List[Dict[str, str]]] = None) -> None:
        error = f"Location with name '{name}' already exists at coordinates ({longitude}, {latitude})"
        if details is None:
            details = [
                {"field": "name", "message": f"Location with name '{name}' already exists"},
                {"field": "coordinates", "message": f"Coordinates ({longitude}, {latitude}) already in use"}
            ]
        super().__init__(status_code=409, error=error, details=details)


class DuplicateCategoryError(MapMyWorldException):
    """Duplicate category error."""
    
    def __init__(self, name: str, details: Optional[List[Dict[str, str]]] = None) -> None:
        error = f"Category with name '{name}' already exists"
        if details is None:
            details = [{"field": "name", "message": f"Category with name '{name}' already exists"}]
        super().__init__(status_code=409, error=error, details=details) 