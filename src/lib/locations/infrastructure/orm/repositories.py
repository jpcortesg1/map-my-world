"""SQLAlchemy repository implementation for locations."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ...domain.entities import Location
from ...domain.repositories import LocationRepository
from .models import LocationModel
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


class LocationRepositoryImpl(LocationRepository):
    """SQLAlchemy implementation of LocationRepository."""
    
    def __init__(self, session: Session) -> None:
        self.session = session
    
    async def create(self, location: Location) -> Location:
        """Create a new location."""
        logger.info(f"Creating location in database: {location.name}")
        
        try:
            location_model = LocationModel.from_domain(location)
            self.session.add(location_model)
            self.session.commit()
            self.session.refresh(location_model)
            
            logger.info(f"Location created in database: {location_model.id}")
            return location_model.to_domain()
        except Exception as e:
            logger.error(f"Error creating location: {e}")
            self.session.rollback()
            raise
    
    async def get_by_id(self, location_id: int) -> Optional[Location]:
        """Get location by ID."""
        logger.info(f"Getting location from database: {location_id}")
        
        location_model = self.session.query(LocationModel).filter(LocationModel.id == location_id).first()
        
        if location_model:
            logger.info(f"Location found in database: {location_id}")
            return location_model.to_domain()
        
        logger.warning(f"Location not found in database: {location_id}")
        return None
    
    async def get_all(
        self, 
        limit: Optional[int] = None,
        offset: int = 0,
        name_filter: Optional[str] = None
    ) -> List[Location]:
        """Get all locations with optional filtering and pagination."""
        logger.info(f"Getting locations from database: limit={limit}, offset={offset}, name_filter={name_filter}")
        
        query = self.session.query(LocationModel)
        
        # Apply name filter if provided
        if name_filter:
            query = query.filter(LocationModel.name.ilike(f"%{name_filter}%"))
        
        # Apply ordering for consistent pagination
        query = query.order_by(LocationModel.id)
        
        # Apply offset
        if offset > 0:
            query = query.offset(offset)
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        location_models = query.all()
        locations = [model.to_domain() for model in location_models]
        
        logger.info(f"Retrieved {len(locations)} locations from database")
        return locations
    
    async def update(self, location: Location) -> Location:
        """Update an existing location."""
        logger.info(f"Updating location in database: {location.id}")
        
        location_model = self.session.query(LocationModel).filter(LocationModel.id == location.id).first()
        
        if not location_model:
            logger.warning(f"Location not found for update: {location.id}")
            return None
        
        # Update fields
        location_model.name = location.name
        location_model.longitude = location.longitude
        location_model.latitude = location.latitude
        location_model.description = location.description
        location_model.updated_at = location.updated_at
        
        self.session.commit()
        self.session.refresh(location_model)
        
        logger.info(f"Location updated in database: {location.id}")
        return location_model.to_domain()
    
    async def delete(self, location_id: int) -> bool:
        """Delete a location by ID."""
        logger.info(f"Deleting location from database: {location_id}")
        
        location_model = self.session.query(LocationModel).filter(LocationModel.id == location_id).first()
        
        if not location_model:
            logger.warning(f"Location not found for deletion: {location_id}")
            return False
        
        self.session.delete(location_model)
        self.session.commit()
        
        logger.info(f"Location deleted from database: {location_id}")
        return True
    
    async def exists_by_name_and_coordinates(self, name: str, longitude: float, latitude: float) -> bool:
        """Check if location exists by name and coordinates."""
        logger.info(f"Checking if location exists: {name} at ({longitude}, {latitude})")
        
        exists = self.session.query(LocationModel).filter(
            and_(
                LocationModel.name == name,
                LocationModel.longitude == longitude,
                LocationModel.latitude == latitude
            )
        ).first() is not None
        
        logger.info(f"Location exists check result: {exists}")
        return exists 