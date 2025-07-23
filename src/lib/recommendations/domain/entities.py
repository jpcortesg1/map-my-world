"""Domain entities for recommendations."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LocationCategoryReview:
    """LocationCategoryReview domain entity."""
    
    id: int
    location_id: int
    category_id: int
    reviewed_at: Optional[datetime]
    created_at: datetime
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "location_id": self.location_id,
            "category_id": self.category_id,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "created_at": self.created_at.isoformat(),
        } 