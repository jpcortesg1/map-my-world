"""DTOs for categories application layer."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CategoryCreateDTO:
    """DTO for creating a category."""
    
    name: str
    description: Optional[str] = None


@dataclass
class CategoryResponseDTO:
    """DTO for category response."""
    
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, category) -> "CategoryResponseDTO":
        """Create DTO from domain entity."""
        return cls(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )


@dataclass
class CategoryFilterDTO:
    """DTO for filtering categories."""
    
    name: Optional[str] = None 