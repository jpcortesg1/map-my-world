"""Repository interfaces for locations domain."""
from typing import Protocol, List, Optional
from .entities import Location


class LocationRepository(Protocol):
    """Repository interface for location operations."""
    
    async def create(self, location: Location) -> Location:
        """Create a new location."""
        ...
    
    async def get_by_id(self, location_id: int) -> Optional[Location]:
        """Get location by ID."""
        ...
    
    async def get_all(
        self, 
        limit: Optional[int] = None,
        offset: int = 0,
        name_filter: Optional[str] = None
    ) -> List[Location]:
        """Get all locations with optional filtering and pagination."""
        ...
    
    async def update(self, location: Location) -> Location:
        """Update an existing location."""
        ...
    
    async def delete(self, location_id: int) -> bool:
        """Delete a location by ID."""
        ...
    
    async def exists_by_name_and_coordinates(self, name: str, longitude: float, latitude: float) -> bool:
        """Check if location exists by name and coordinates."""
        ... 