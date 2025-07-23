"""Pydantic schemas for category API."""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from ...domain.entities import Category
import urllib.parse


class CategoryQueryParams(BaseModel):
    """Query parameters for category endpoints."""
    limit: Optional[int] = Field(
        default=None, 
        ge=1, 
        le=100, 
        description="Number of categories to return (max 100)"
    )
    offset: int = Field(
        default=0, 
        ge=0, 
        description="Number of categories to skip"
    )
    name: Optional[str] = Field(
        default=None, 
        min_length=1, 
        description="Filter by category name (partial match)"
    )
    
    @field_validator('name', mode='before')
    @classmethod
    def decode_name(cls, v):
        """Decode URL-encoded name parameter."""
        if v is not None and isinstance(v, str):
            try:
                return urllib.parse.unquote_plus(v)
            except Exception:
                return v
        return v


class CategoryCreateSchema(BaseModel):
    """Schema for creating a category."""
    name: str = Field(..., min_length=1, max_length=255, description="Category name")
    description: Optional[str] = Field(None, description="Category description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Restaurants",
                "description": "Places to eat and dine"
            }
        }
    }


class CategoryUpdateSchema(BaseModel):
    """Schema for updating a category."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Category name")
    description: Optional[str] = Field(None, description="Category description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Restaurants Updated",
                "description": "Updated description for restaurants"
            }
        }
    }


class CategoryResponseSchema(BaseModel):
    """Schema for category responses."""
    id: int = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    @classmethod
    def from_domain(cls, category: Category) -> "CategoryResponseSchema":
        """Create schema from domain entity."""
        return cls(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at.isoformat(),
            updated_at=category.updated_at.isoformat()
        )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Restaurants",
                "description": "Places to eat and dine",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    } 