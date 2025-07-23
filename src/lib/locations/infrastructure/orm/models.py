"""SQLAlchemy models for locations."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from config.database import Base
from ...domain.entities import Location
from ...domain.value_objects import Coordinates


class LocationModel(Base):
    """SQLAlchemy model for locations table."""
    
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_domain(self) -> Location:
        """Convert model to domain entity."""
        coordinates = Coordinates(longitude=self.longitude, latitude=self.latitude)
        return Location(
            id=self.id,
            coordinates=coordinates,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain(cls, location: Location) -> "LocationModel":
        """Create model from domain entity."""
        model = cls(
            name=location.name,
            longitude=location.longitude,
            latitude=location.latitude,
            description=location.description,
            created_at=location.created_at,
            updated_at=location.updated_at
        )
        # Only set id if it's not None (for updates)
        if location.id is not None:
            model.id = location.id
        return model 