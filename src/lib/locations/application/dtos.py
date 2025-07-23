"""DTOs for locations application layer."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LocationCreateDTO:
    """DTO for creating a location."""
    
    name: str
    longitude: float
    latitude: float
    description: Optional[str] = None


@dataclass
class LocationResponseDTO:
    """DTO for location response."""
    
    id: int
    name: str
    longitude: float
    latitude: float
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, location) -> "LocationResponseDTO":
        """Create DTO from domain entity."""
        return cls(
            id=location.id,
            name=location.name,
            longitude=location.longitude,
            latitude=location.latitude,
            description=location.description,
            created_at=location.created_at,
            updated_at=location.updated_at,
        )


@dataclass
class LocationFilterDTO:
    """DTO for filtering locations."""
    
    name: Optional[str] = None
    min_latitude: Optional[float] = None
    max_latitude: Optional[float] = None
    min_longitude: Optional[float] = None
    max_longitude: Optional[float] = None 