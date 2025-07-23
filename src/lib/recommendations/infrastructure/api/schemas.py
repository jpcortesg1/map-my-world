"""Pydantic schemas for recommendations API."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RecommendationResponseSchema(BaseModel):
    """Schema for recommendation response."""
    
    location_id: int = Field(..., description="Location ID")
    location_name: str = Field(..., description="Location name")
    longitude: float = Field(..., description="Longitude coordinate")
    latitude: float = Field(..., description="Latitude coordinate")
    category_id: int = Field(..., description="Category ID")
    category_name: str = Field(..., description="Category name")
    reviewed_at: Optional[datetime] = Field(None, description="When this combination was last reviewed")
    
    class Config:
        schema_extra = {
            "example": {
                "location_id": 1,
                "location_name": "Central Park",
                "longitude": -73.935242,
                "latitude": 40.782865,
                "category_id": 1,
                "category_name": "Restaurants",
                "reviewed_at": None
            }
        }


class MarkAsReviewedSchema(BaseModel):
    """Schema for marking a combination as reviewed."""
    
    location_id: int = Field(..., description="Location ID")
    category_id: int = Field(..., description="Category ID")
    
    class Config:
        schema_extra = {
            "example": {
                "location_id": 1,
                "category_id": 1
            }
        } 