"""DTOs for recommendations application layer."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RecommendationResponseDTO:
    """DTO for recommendation response."""
    
    location_id: int
    location_name: str
    longitude: float
    latitude: float
    category_id: int
    category_name: str
    reviewed_at: Optional[datetime]
    
    @classmethod
    def from_domain(cls, location, category, reviewed_at: Optional[datetime] = None) -> "RecommendationResponseDTO":
        """Create DTO from domain entities."""
        return cls(
            location_id=location.id,
            location_name=location.name,
            longitude=location.longitude,
            latitude=location.latitude,
            category_id=category.id,
            category_name=category.name,
            reviewed_at=reviewed_at,
        )


@dataclass
class MarkAsReviewedDTO:
    """DTO for marking a combination as reviewed."""
    
    location_id: int
    category_id: int 