"""Pydantic schemas for location API."""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from ...domain.entities import Location
import urllib.parse


class LocationQueryParams(BaseModel):
    """Query parameters for location endpoints."""
    limit: Optional[int] = Field(
        default=None, 
        ge=1, 
        le=100, 
        description="Number of locations to return (max 100)"
    )
    offset: int = Field(
        default=0, 
        ge=0, 
        description="Number of locations to skip"
    )
    name: Optional[str] = Field(
        default=None, 
        min_length=1, 
        description="Filter by location name (partial match)"
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


class LocationCreateSchema(BaseModel):
    """Schema for creating a location."""
    name: str = Field(..., min_length=1, max_length=255, description="Location name")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    description: Optional[str] = Field(None, description="Location description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Central Park",
                "longitude": -73.9654,
                "latitude": 40.7829,
                "description": "Large public park in New York City"
            }
        }
    }


class LocationUpdateSchema(BaseModel):
    """Schema for updating a location."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Location name")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    description: Optional[str] = Field(None, description="Location description")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Central Park Updated",
                "description": "Updated description for Central Park"
            }
        }
    }


class LocationResponseSchema(BaseModel):
    """Schema for location responses."""
    id: int = Field(..., description="Location ID")
    name: str = Field(..., description="Location name")
    longitude: float = Field(..., description="Longitude coordinate")
    latitude: float = Field(..., description="Latitude coordinate")
    description: Optional[str] = Field(None, description="Location description")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    @classmethod
    def from_domain(cls, location: Location) -> "LocationResponseSchema":
        """Create schema from domain entity."""
        return cls(
            id=location.id,
            name=location.name,
            longitude=location.longitude,
            latitude=location.latitude,
            description=location.description,
            created_at=location.created_at.isoformat(),
            updated_at=location.updated_at.isoformat()
        )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Central Park",
                "longitude": -73.9654,
                "latitude": 40.7829,
                "description": "Large public park in New York City",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    }


class LocationFilterSchema(BaseModel):
    """Schema for filtering locations."""
    
    name: Optional[str] = Field(None, description="Filter by name (partial match)")
    min_latitude: Optional[float] = Field(None, ge=-90, le=90, description="Minimum latitude")
    max_latitude: Optional[float] = Field(None, ge=-90, le=90, description="Maximum latitude")
    min_longitude: Optional[float] = Field(None, ge=-180, le=180, description="Minimum longitude")
    max_longitude: Optional[float] = Field(None, ge=-180, le=180, description="Maximum longitude")
    
    @classmethod
    def validate_latitude_range(cls, v, values):
        """Validate latitude range."""
        if v is not None and 'min_latitude' in values and 'max_latitude' in values:
            min_lat = values.get('min_latitude')
            max_lat = values.get('max_latitude')
            if min_lat is not None and max_lat is not None and min_lat > max_lat:
                raise ValueError("min_latitude cannot be greater than max_latitude")
        return v
    
    @classmethod
    def validate_longitude_range(cls, v, values):
        """Validate longitude range."""
        if v is not None and 'min_longitude' in values and 'max_longitude' in values:
            min_lon = values.get('min_longitude')
            max_lon = values.get('max_longitude')
            if min_lon is not None and max_lon is not None and min_lon > max_lon:
                raise ValueError("min_longitude cannot be greater than max_longitude")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "park",
                "min_latitude": 40.0,
                "max_latitude": 41.0,
                "min_longitude": -74.0,
                "max_longitude": -73.0
            }
        }
    } 