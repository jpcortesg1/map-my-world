"""Value objects for locations domain."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Coordinates:
    """Value object for geographic coordinates."""
    
    longitude: float
    latitude: float
    
    def __post_init__(self) -> None:
        """Validate coordinates after initialization."""
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
    
    def __str__(self) -> str:
        """String representation of coordinates."""
        return f"({self.longitude}, {self.latitude})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "longitude": self.longitude,
            "latitude": self.latitude
        } 