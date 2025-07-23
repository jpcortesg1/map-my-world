"""Domain entities for categories."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Category:
    """Category domain entity."""
    
    id: Optional[int]
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        } 