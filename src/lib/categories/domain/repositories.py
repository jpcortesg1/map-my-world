"""Repository interfaces for categories domain."""
from typing import Protocol, List, Optional
from .entities import Category


class CategoryRepository(Protocol):
    """Repository interface for category operations."""
    
    async def create(self, category: Category) -> Category:
        """Create a new category."""
        ...
    
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        ...
    
    async def get_all(
        self, 
        limit: Optional[int] = None,
        offset: int = 0,
        name_filter: Optional[str] = None
    ) -> List[Category]:
        """Get all categories with optional filtering and pagination."""
        ...
    
    async def update(self, category: Category) -> Category:
        """Update an existing category."""
        ...
    
    async def delete(self, category_id: int) -> bool:
        """Delete a category by ID."""
        ...
    
    async def exists_by_name(self, name: str) -> bool:
        """Check if category exists by name."""
        ... 