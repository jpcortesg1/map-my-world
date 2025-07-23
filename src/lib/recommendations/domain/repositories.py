"""Repository interfaces for recommendations domain."""
from typing import Protocol, List
from .entities import LocationCategoryReview


class RecommendationRepository(Protocol):
    """Repository interface for recommendation operations."""
    
    async def get_unreviewed_combinations(self, limit: int = 10) -> List[dict]:
        """Get location-category combinations not reviewed in the last 30 days."""
        ...
    
    async def mark_as_reviewed(self, location_id: int, category_id: int) -> LocationCategoryReview:
        """Mark a location-category combination as reviewed."""
        ...
    
    async def get_reviewed_combinations(self, location_id: int, category_id: int) -> List[LocationCategoryReview]:
        """Get reviewed combinations for a specific location and category."""
        ...
    
    async def check_location_exists(self, location_id: int) -> bool:
        """Check if a location exists by ID."""
        ...
    
    async def check_category_exists(self, category_id: int) -> bool:
        """Check if a category exists by ID."""
        ... 