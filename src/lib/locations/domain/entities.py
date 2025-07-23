"""Domain entities for locations."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .value_objects import Coordinates


@dataclass
class Location:
    """Location domain entity."""
    
    id: Optional[int]
    coordinates: Coordinates
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @property
    def longitude(self) -> float:
        """Get longitude from coordinates."""
        return self.coordinates.longitude
    
    @property
    def latitude(self) -> float:
        """Get latitude from coordinates."""
        return self.coordinates.latitude
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        } 